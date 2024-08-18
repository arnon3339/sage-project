from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers
from django.db import IntegrityError
from django.db.models import Count
from ..models import Link, Category, Tag
import requests
import json
from bs4 import BeautifulSoup

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # The user is authenticated, and we can access the user object
        username = request.user.username
        return Response({"username": username})

class FavLink(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # username = request.user.username
        found_links = Link.objects.filter(user=request.user)
        found_links = serializers.serialize('json', found_links)
        found_links_json = json.loads(found_links)
        # print(found_links)
        return Response({"data": found_links_json})
        # return Response({"data": "found_links"})
    
    def post(self, request, *args, **kwargs):
        try:
            data_body = json.loads(request.body)
            response = requests.get(data_body["url"])

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
        except:
            title = data_body["url"]
        finally:
            # username = request.user.username
            try:
                link = Link.objects.create(
                    user=request.user,
                    title=title,
                    url=data_body["url"],
                )
                added_link = serializers.serialize('json', [link])
                added_link_json = json.loads(added_link)

                if "category" in data_body:
                    for cat in data_body["category"]:
                        try:
                            Category.objects.create(
                                link=link,
                                category=cat,
                            )
                        except IntegrityError:
                            continue
                        except:
                            return Response({'error': 'Adding link error'}, status=status.HTTP_404_NOT_FOUND)

                if "tag" in data_body:
                    for tag in data_body["tag"]:
                        try:
                            Tag.objects.create(
                                link=link,
                                tag=tag,
                            )
                        except IntegrityError:
                            continue
                        except:
                            return Response({'error': 'Adding link error'}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError:
                return Response({'error': 'already exist Url'}, status=status.HTTP_409_CONFLICT)
            except:
                return Response({'error': 'Adding link error'}, status=status.HTTP_404_NOT_FOUND)
                
            return Response({"data": added_link_json})

class FavlinkExistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, kind, *args, **kwargs):
        user = request.user 
        try: 
            if kind == "category":
                category_link_counts = Link.objects.filter(user=user) \
                                   .values('category__category') \
                                    .exclude(category__isnull=True)\
                                   .annotate(link_count=Count('id'))
                return Response({"data": category_link_counts})
            elif kind == "tag":
                tag_link_counts = Link.objects.filter(user=user) \
                                   .values('tag__tag') \
                                    .exclude(tag__isnull=True)\
                                   .annotate(link_count=Count('id'))
                return Response({"data": tag_link_counts})
            else:
                return Response({'error': 'Viewing categories or tags error'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            return Response({'error': 'Viewing categories or tags error'}, status=status.HTTP_404_NOT_FOUND)

class FavlinkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, kind, *args, **kwargs):
        try:
            data_body = json.loads(request.body)
            if kind == "link":
                if "url" in data_body and data_body["url"] != "":
                    link = Link.objects.get(url=data_body["url"], user=request.user).delete()
                    return Response({"data": link})
                else:
                    return Response({'error': 'Empty Url'}, status=status.HTTP_404_NOT_FOUND)
            else:
                link = Link.objects.get(url=data_body["url"], user=request.user)
                if kind == "category":
                    try:
                        cat = Category.objects.filter(
                            link=link,
                            category__in=data_body["category"],
                        ).delete()
                    except:
                        return Response({'error': 'Deleting category error'}, status=status.HTTP_404_NOT_FOUND)

                if kind == "tag":
                    try:
                        tag = Tag.objects.filter(
                            link=link,
                            tag__in=data_body["tag"],
                        ).delete()
                    except:
                        return Response({'error': 'Deleting tag error'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'Deleting link error'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            return Response({"data": link})

class FavlinkUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data_body = json.loads(request.body)
            if "url" not in data_body or data_body["url"] == "":
                return Response({'error': 'Updating error without Url'}, status=status.HTTP_404_NOT_FOUND)

            link = Link.objects.get(user=user, url=data_body["url"])
            if "title" in data_body:
                link.title = data_body["title"]

            if "url" in data_body:
                link.url = data_body["url"]

            if "category" in data_body:
                for cat in data_body["category"]:
                    try:
                        Category.objects.create(
                            link=link,
                            category=cat,
                        )
                    except IntegrityError:
                        continue
                    except:
                        return Response({'error': 'Updating category error'}, status=status.HTTP_404_NOT_FOUND)

            if "tag" in data_body:
                for tag in data_body["tag"]:
                    try:
                        Tag.objects.create(
                            link=link,
                            tag=tag,
                        )
                    except IntegrityError:
                        continue
                    except:
                        return Response({'error': 'Updating tag error'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'Updating error'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            return Response({"data": link})

class FavlinkEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data_body = json.loads(request.body)
            if "url" not in data_body or data_body["url"] == "":
                return Response({'error': 'Updating error without Url'}, status=status.HTTP_404_NOT_FOUND)

            link = Link.objects.get(user=user, url=data_body["url"])

            if "category_old" in data_body and "category_new" in data_body:
                for cat_old, cat_new in zip(data_body["category_old", "category_new"]):
                    try:
                        Category.objects.filter(
                            link=link,
                            category=cat_old,
                        ).update(
                            category=cat_new,
                        )
                    except:
                        return Response({'error': 'Editing category error'}, status=status.HTTP_404_NOT_FOUND)

            if "tag_old" in data_body and "tag_new" in data_body:
                for tag_old, tag_new in zip(data_body["tag_old", "tag_new"]):
                    try:
                        Tag.objects.filter(
                            link=link,
                            tag=tag_old,
                        ).update(
                            tag=tag_new
                        )
                    except IntegrityError:
                        continue
                    except:
                        return Response({'error': 'Editing tag error'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'Editing error'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            return Response({"data": link})

class FavlinkKeywordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            keyword = request.GET.get('q')
            category = request.GET.get('cat')
            tag = request.GET.get('tag')
            page = request.GET.get('page')
            num = request.GET.get('n') if request.GET.get('n') else 20
            return Response({"data": keyword})
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_404_NOT_FOUND)
