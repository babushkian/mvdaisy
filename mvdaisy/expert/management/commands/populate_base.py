from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model;
from main.models import Rank, RankType, RankAndType,  Position
from expert.models import Laboratory, ExpertiseArea, ExpertExpertiseArea,  ExpertLaboratory


class Command(BaseCommand):
    help = "Наполняет базу первоначальными значениями"
    
    def handle(self, *args, **options):
        ranks = ["младший лейтенант", "лейтенант", "старший лейтенант", "капитан", "майор", "подполковник",
                 "полковник", "рядовой", "вольный найм", "госслужащий"]
        ranktypes = ["полиции", "юстиции", "внутренней службы", "армии", "ФСБ", "гражданский"]
        rank_rank_type = [(10, 1), (3,2), (8,5), (6,2), (1,5), (8,1), (4,1), (5,1), (8,4), (7,4), (9,6), (10,6),
                          (1, 3), (2, 3), (3, 3), (2, 5), (7, 1), (5, 2), (1, 1), (2, 1), (3, 1)]

        positions = ["эксперт", "старший эксперт", "главный эксперт", "начальник отделения", "зам. начальника отдела",
                     "начальник отдела"]

        laboratories = ["компьютерная",       # 1
                        "фоноскопическая",    # 2
                        "автотехническая",    # 3
                        "пожаротехническая",  # 4
                        "радиотехническая"]   # 5

        permissions = [("компьютерная", 1),      # 1
                       ("радиотехническая", 5),  # 2
                       ("лингвистическая", 2),   # 3
                       ("фоноскопическая", 2),   # 4
                       ("автороведческая", 2),   # 5
                       ("автотехническая", 3),   # 6
                       ("трасологическая", 3),   # 7
                       ("пожаротехника", 4),     # 8
                       ("взрывотехника", 4),     # 9
                    ]

        l = []
        for i in ranks:
            l.append(Rank(name=i))
        Rank.objects.bulk_create(l)

        l = []
        for i in ranktypes:
            l.append(RankType(name=i))
        RankType.objects.bulk_create(l)

        for i in rank_rank_type:
            RankAndType.objects.create(rank=Rank.objects.get(pk=i[0]), type=RankType.objects.get(pk=i[1]))

        l = []
        for i in positions:
            l.append(Position(name=i))
        Position.objects.bulk_create(l)

        l = []
        for i in laboratories:
            l.append(Laboratory(name=i))
        Laboratory.objects.bulk_create(l)

        l = []
        for i in permissions:
            l.append(ExpertiseArea(name=i[0], laboratory=Laboratory.objects.get(pk=i[1])))
        ExpertiseArea.objects.bulk_create(l)

        expert_laboratory = [
            {"username": "gusak", "laboratory": 1, "start_date": date(2011, 1, 1), "end_date": date(2023, 9, 1)},
            {"username":"goelov", "laboratory": 1, "start_date": date(2012, 3, 1), "end_date": None},
            {"username": "popich", "laboratory": 2, "start_date": date(2020, 8, 12), "end_date": None},
            {"username": "kurduk", "laboratory": 3, "start_date": date(2012, 11, 13), "end_date": date(2016, 8, 7)},
            {"username": "kurduk", "laboratory": 2, "start_date": date(2016, 8, 8), "end_date": None},
            {"username": "kurduk", "laboratory": 3, "start_date": date(2018, 4, 5), "end_date": None},
            {"username": "pelmesh", "laboratory": 1, "start_date": date(2013, 2, 11), "end_date": None},
            {"username": "taran", "laboratory": 1, "start_date": date(2017, 8, 19), "end_date": None},
            {"username": "taran", "laboratory": 5, "start_date": date(2016, 11, 3), "end_date": None},
            {"username": "cheese", "laboratory": 2, "start_date": date(2012, 10, 10), "end_date": None},
            {"username": "pyramid", "laboratory": 4, "start_date": date(2011, 9, 10), "end_date": None},
            {"username": "gril", "laboratory": 2, "start_date": date(2021, 11, 8), "end_date": None}]

        users_list = [
            {"username": "gusak", "password": "1234", "first_name": "Дмитрий", "second_name": "Александрович", "last_name": "Гусак", "sex": 1,
             "working": 0, "position_id": 2, "rank_id": 5, "rank_type_id": 1, },
            {"username": "goelov", "password": "1234", "first_name": "Дмитрий", "second_name": "Константинович", "last_name": "Гоелов", "sex": 1,
             "working": 1, "position_id": 3, "rank_id": 5, "rank_type_id": 1, },
            {"username": "popich", "password": "1234", "first_name": "Яна", "second_name": "Викторовна", "last_name": "Попыщева", "sex": 0,
            "working":1,  "position_id": 1, "rank_id":3, "rank_type_id": 1,},
            {"username": "kurduk", "password": "1234", "first_name": "Илья", "second_name": "Валерьевич", "last_name": "Курдюкбаев", "sex": 1,
             "working": 1, "position_id": 2, "rank_id": 4, "rank_type_id": 1, },
            {"username": "taran", "password": "1234", "first_name": "Константин", "second_name": "Константинович", "last_name": "Таран", "sex": 1,
             "working": 1, "position_id": 1, "rank_id": 4, "rank_type_id": 1, },
            {"username": "cheese", "password": "1234","first_name": "Наталья", "second_name": "Викторовна", "last_name": "Троесырова", "sex":0, 
             "working":1,  "position_id": 3, "rank_id":4, "rank_type_id": 1,},
            {"username": "pyramid", "password": "1234", "first_name": "Маским", "second_name": "Андреевич", "last_name": "Пирамидкин", "sex": 1,
             "working": 1, "position_id": 5, "rank_id": 6, "rank_type_id": 1, },

            {"username": "pelmesh", "password": "1234", "first_name": "Алексей", "second_name": "Сергеевич",
             "last_name": "Пельмешко", "sex": 1, "working": 1, "position_id": 2, "rank_id": 5, "rank_type_id": 1, },
            {"username": "gril", "password": "1234", "first_name": "Виктория", "second_name": "Владимировна",
             "last_name": "Грильяж", "sex": 0, "working": 1, "position_id": 1, "rank_id": 2, "rank_type_id": 1, },
            {"username": "mansur", "password": "1234", "first_name": "Сергей", "second_name": "Геннадьевич",
             "last_name": "Мансуров", "sex": 1, "working": 1, "position_id": 6, "rank_id": 7, "rank_type_id": 1, },

        ]

        expert_permission = [{"username": "gusak", "permission_id": 1, "start_date": date(2019, 5, 5), "end_date": date(2024, 5, 5)},
                    {"username": "goelov", "permission_id": 1, "start_date": date(2017, 1, 1), "end_date": date(2022, 1, 1)},
                    {"username": "goelov", "permission_id": 1, "start_date": date(2021, 11, 21), "end_date": date(2026, 11, 21)},
                    {"username": "popich", "permission_id": 3, "start_date": date(2022, 6, 15), "end_date": date(2027, 6, 15)},
                    {"username": "popich", "permission_id": 4, "start_date": date(2023, 3, 15), "end_date": date(2028, 3, 15)},
                    {"username": "kurduk", "permission_id": 4, "start_date": date(2021, 3, 15), "end_date": date(2026, 3, 15)},
                    {"username": "kurduk", "permission_id": 6, "start_date": date(2022, 3, 22), "end_date": date(2027, 3, 22)},
                    {"username": "taran", "permission_id": 1, "start_date": date(2018, 7, 25),  "end_date": date(2023, 7, 25)},
                    {"username": "taran", "permission_id": 1, "start_date": date(2023, 4, 22), "end_date": date(2028, 4, 22)},
                    {"username": "taran", "permission_id": 2, "start_date": date(2023, 6, 12), "end_date": date(2028, 6, 12)},
                    {"username": "cheese", "permission_id": 3, "start_date": date(2021, 3, 15), "end_date": date(2026, 3, 15)},
                    {"username": "cheese", "permission_id": 4, "start_date": date(2023, 6, 12), "end_date": date(2028, 6, 12)},
                    {"username": "cheese", "permission_id": 5, "start_date": date(2019, 10, 1), "end_date": date(2024, 10, 1)},
                    {"username": "pyramid", "permission_id": 8, "start_date": date(2021, 4, 29), "end_date": date(2026, 4, 29)},
                    {"username": "pyramid", "permission_id": 9, "start_date": date(2022, 9, 1), "end_date": date(2026, 9, 1)},
                    {"username": "pelmesh", "permission_id": 1, "start_date": date(2024, 6, 1), "end_date": date(2029, 6, 1)},
                    {"username": "gril", "permission_id": 4, "start_date": date(2023, 12, 15), "end_date": date(2028, 12, 15)},
                    ]


        User = get_user_model()
        User.objects.create_superuser('admin', 'admin@myproject.com', '1234', last_name="admin", working=False)
        for user in users_list:
            User.objects.create_user(**user)


        for i in expert_laboratory:
            ExpertLaboratory.objects.create(expert=User.objects.get(username=i["username"]),
                                            laboratory=Laboratory.objects.get(pk=i["laboratory"]),
                                            start_date=i["start_date"],
                                            end_date=i["end_date"],
                                            )

        for i in expert_permission:
            ExpertExpertiseArea.objects.create(expert=User.objects.get(username=i["username"]),
                                               expertisearea=ExpertiseArea.objects.get(pk=i["permission_id"]),
                                               start_date=i["start_date"],
                                               end_date=i["end_date"],
                                               )


