from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from .models import Game
import requests
import os
from game_analytics import settings
from datetime import datetime
import logging
from django.db.models import Max, Min, Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

logger = logging.getLogger(__name__)

class UploadCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        csv_url = request.data.get('csv_url')


        if not csv_url:
            return Response({"message": "CSV URL is required"}, status=400)

        try:
            csv_url = csv_url.strip().strip("'")
            if not csv_url.startswith(('http://', 'https://')):
                return Response({"message": "Invalid CSV URL format"}, status=400)

            logger.info(f"Fetching CSV data from URL: {csv_url}")
            response = requests.get(csv_url, stream=True)
            response.raise_for_status()

            file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_csv.csv')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            logger.info(f"Saving CSV file to {file_path}")

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            chunk_size = 20000
            logger.info(f"Processing CSV file in chunks of size {chunk_size}")

            all_games = []
            for chunk in pd.read_csv(file_path, encoding='utf-8', chunksize=chunk_size):
                for _, row in chunk.iterrows():
                    if 'AppID' not in row or 'Name' not in row or 'Release date' not in row:
                        logger.error(f"CSV missing required columns.")
                        raise ValueError("CSV file must contain 'AppID', 'Name', and 'Release date' columns.")

                    if not pd.notna(row['AppID']) or not pd.notna(row['Name']) or not pd.notna(row['Release date']):
                        logger.error(f"CSV row has missing required fields: {row}")
                        continue

                    app_id = int(row['AppID'])
                    name = row['Name']
                    release_date = self.parse_date(row['Release date'])
                    score_rank = row['Score rank'] if pd.notna(row['Score rank']) else None

                    game_data = {
                        'app_id': app_id,
                        'defaults': {
                            'name': name,
                            'release_date': release_date,
                            'required_age': row.get('Required age', None),
                            'price': row.get('Price', None),
                            'dlc_count': row.get('DLC count', None),
                            'about_the_game': row.get('About the game', None),
                            'supported_languages': row.get('Supported languages', []),
                            'windows': row.get('Windows', 'FALSE') == 'TRUE',
                            'mac': row.get('Mac', 'FALSE') == 'TRUE',
                            'linux': row.get('Linux', 'FALSE') == 'TRUE',
                            'positive_reviews': row.get('Positive', 0),
                            'negative_reviews': row.get('Negative', 0),
                            'score_rank': score_rank,
                            'developers': row.get('Developers', None),
                            'publishers': row.get('Publishers', None),
                            'categories': row.get('Categories', None),
                            'genres': row.get('Genres', None),
                            'tags': row.get('Tags', None),
                        }
                    }

                    all_games.append(game_data)

            # Retrieve existing games in bulk and create a lookup dictionary
            existing_games = Game.objects.filter(app_id__in=[game['app_id'] for game in all_games])
            existing_games_dict = {game.app_id: game for game in existing_games}

            games_to_create = []
            games_to_update = []

            for game in all_games:
                if game['app_id'] in existing_games_dict:
                    existing_game = existing_games_dict[game['app_id']]
                    for key, value in game['defaults'].items():
                        setattr(existing_game, key, value)
                    games_to_update.append(existing_game)
                else:
                    games_to_create.append(Game(app_id=game['app_id'], **game['defaults']))

            # Use bulk operations to update and create games
            with transaction.atomic():
                if games_to_create:
                    Game.objects.bulk_create(games_to_create, ignore_conflicts=True)
                if games_to_update:
                    Game.objects.bulk_update(games_to_update, fields=list(game['defaults'].keys()))

            return Response({"message": "CSV uploaded and processed successfully"})
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return Response({"message": f"Failed to fetch CSV from URL: {str(e)}"}, status=400)
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            return Response({"message": str(e)}, status=400)
        except Exception as e:
            logger.error(f"General error: {str(e)}")
            return Response({"message": f"Failed to upload CSV: {str(e)}"}, status=400)

    def parse_date(self, date_str):
        try:
            formats = ['%b %d, %Y', '%d %b %Y', '%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%b %Y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Date format for '{date_str}' is not recognized")
        except Exception as e:
            raise ValueError(f"Failed to parse date: {str(e)}")


class QueryData(APIView):
    permission_classes = [IsAuthenticated]  # Add authentication check
    
    def get(self, request, *args, **kwargs):
        filters = request.GET
        print(f"Request filters: {filters}")

        # Initialize the queryset
        queryset = Game.objects.all()
        aggregate_queries = {}

        # Process aggregate queries first
        for field, value in filters.items():
            if field.startswith('aggregate_'):  # Aggregate queries
                aggregate_field = field[len('aggregate_'):]  # Strip 'aggregate_' prefix

                if aggregate_field == 'max_price':
                    max_price = queryset.aggregate(max_price=Max('price'))['max_price']
                    aggregate_queries['max_price'] = max_price
                elif aggregate_field == 'min_price':
                    min_price = queryset.aggregate(min_price=Min('price'))['min_price']
                    aggregate_queries['min_price'] = min_price
                elif aggregate_field == 'mean_price':
                    mean_price = queryset.aggregate(mean_price=Avg('price'))['mean_price']
                    mean_price_rounded = round(mean_price, 3)
                    aggregate_queries['mean_price'] = mean_price_rounded
                else:
                    return Response({'message': f'Unsupported aggregate query {aggregate_field}.'}, status=status.HTTP_400_BAD_REQUEST)

        # Apply filters to the queryset
        for field, value in filters.items():
            if field.startswith('aggregate_'):
                continue  # Skip aggregate queries as they are already processed
            
            elif field in ['required_age', 'release_date', 'price']:  # Numerical or date fields
                if field == 'required_age':
                    try:
                        value = int(value)
                        queryset = queryset.filter(**{f'{field}': value})
                    except ValueError:
                        return Response({'message': 'Invalid age filter value. Must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
                elif field == 'price':  # Handle 'price' filter
                    try:
                        price_list = [float(v) for v in value.split(',') if v]  # Convert comma-separated values to list of floats
                        if len(price_list) == 1:
                            queryset = queryset.filter(price=price_list[0])  # Single price filter
                        elif len(price_list) > 1:
                            queryset = queryset.filter(price__in=price_list)  # Multiple prices filter
                    except ValueError:
                        return Response({'message': 'Invalid price filter value. Must be a number.'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif field.startswith('date_'):  # Date range queries
                date_filter = field[len('date_'):]  # Strip 'date_' prefix
                if date_filter == 'gt':
                    try:
                        date_value = datetime.strptime(value, '%Y-%m-%d')
                        queryset = queryset.filter(release_date__gt=date_value)
                    except ValueError:
                        return Response({'message': 'Invalid date format for date_gt filter. Must be YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
                elif date_filter == 'lt':
                    try:
                        date_value = datetime.strptime(value, '%Y-%m-%d')
                        queryset = queryset.filter(release_date__lt=date_value)
                    except ValueError:
                        return Response({'message': 'Invalid date format for date_lt filter. Must be YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': f'Unsupported date query {date_filter}.'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif field in [f.name for f in Game._meta.get_fields() if isinstance(f, models.CharField)]:  # String fields
                queryset = queryset.filter(**{f'{field}__icontains': value})
            
            else:
                return Response({'message': f'Field {field} does not exist or is not a valid field for filtering.'}, status=status.HTTP_400_BAD_REQUEST)

        results = list(queryset.values())

        response_data = {
            'results': results,
            'aggregates': aggregate_queries if aggregate_queries else None  # Add aggregate queries to response
        }
        return Response(response_data, status=status.HTTP_200_OK)
