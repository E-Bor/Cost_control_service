import csv
import os.path
import zipfile
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from src.apps.cost_controll_app.schemas.schemas import User
from src.database.data_schemes.data_schemas import Expenses, Earnings
from src.database.data_schemes.work_with_db import get_session


class MassOperations:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.data_fields_expense = ("operation_id", "cost", "disc", "date", "category")
        self.data_fields_earnings = ("earning_id", "earning_value", "date")

    def read_database(self, user_id: int) -> dict:

        exp = self.session.query(Expenses.operation_id, Expenses.cost, Expenses.disc, Expenses.date, Expenses.category
                                 ).filter(user_id == user_id).all()

        earn = self.session.query(Earnings.earning_id, Earnings.earning_value, Earnings.date
                                  ).filter(user_id == user_id).all()

        data_dict = {
            "expenses": exp,
            "earnings": earn
        }
        return data_dict

    def create_zip_with_csv(self, data_dict: dict, user_id: int) -> dict:
        with open(f"{user_id}_expenses.csv", "w+") as csvfile:
            expense_writer = csv.writer(csvfile, delimiter=",")
            expense_writer.writerows(data_dict.get("expenses"))

        with open(f"{user_id}_earnings.csv", "w+") as csvfile_2:
            expense_writer = csv.writer(csvfile_2, delimiter=",")
            expense_writer.writerows(data_dict.get("earnings"))
        files = [f"{user_id}_expenses.csv", f"{user_id}_earnings.csv"]

        with zipfile.ZipFile(f"{user_id}_data.zip", "w") as zipped:
            for file in files:
                zipped.write(file)
        file_data = {
            "path": os.path.abspath(f"{user_id}_data.zip"),
            "filename": f"{user_id}_data.zip"
        }
        for _ in files:
            os.remove(os.path.abspath(_))
        return file_data

    def unpack_zip(self, file_name: str) -> list[str]:
        path = os.path.dirname(__file__) + "/uploaded_files/"
        extracted_files = []
        with zipfile.ZipFile(path + file_name) as user_zip:
            user_zip.extractall(path)
            for i in user_zip.namelist():
                if ".csv" in i:
                    extracted_files.append(path + i)
        os.remove(path + file_name)
        return extracted_files


    def read_csv(self, path) -> list[list]:
        with open(path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            list_with_data = [list(i) for i in csv_reader]
        return list_with_data


    def add_data_list_to_db_expenses(self, user: User, data_list: list) -> None:
        data_objs = [Expenses(user_id=user.user_id, operation_id=i[0], cost=i[1], disc=i[2],
                              date=datetime.strptime(i[3], "%Y-%m-%d"),
                              category=i[4])
                     for i in data_list]
        self.session.add_all(data_objs)
        self.session.commit()
        self.session.close()

    def add_data_list_to_db_earnings(self, user: User, data_list: list) -> None:
        data_objs = [Earnings(user_id=user.user_id, earning_id=i[0], earning_value=i[1],
                              date=datetime.strptime(i[2], "%Y-%m-%d"))
                     for i in data_list]
        self.session.add_all(data_objs)
        self.session.commit()
        self.session.close()

    def extract_data_to_db(self, filename: str, user: User):
        unpacked_csv_paths = self.unpack_zip(filename)
        for i in unpacked_csv_paths:
            if f"{user.user_id}_earnings.csv" in i:

                self.add_data_list_to_db_earnings(
                    user,
                    self.read_csv(i)
                )
            if f"{user.user_id}_expenses.csv" in i:

                self.add_data_list_to_db_expenses(
                    user,
                    self.read_csv(i)
                )
