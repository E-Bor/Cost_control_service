import csv
import os.path
import zipfile

from fastapi import Depends
from sqlalchemy.orm import Session

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
        files_to_delete = [os.remove(os.path.abspath(_)) for _ in files]
        return file_data



    def read_csv(self, file_name) -> list:
        with open(f"{file_name}", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            list_with_data = [list(i) for i in csv_reader]
            return list_with_data

    def add_data_list_to_db_expenses(self, data_list: list) -> None:
        data_objs = [Expenses(user_id=i[0], operation_id=i[1], cost=i[2], disc=i[3], date=i[4], category=i[5])
                     for i in data_list]
        self.session.add(data_objs)
        self.session.commit()
        self.session.close()

    def add_data_list_to_db_earnings(self, data_list: list, session: Session) -> None:
        data_objs = [Earnings(user_id=i[0], earning_id=i[1], earning_value=i[2], date=i[3])
                     for i in data_list]
        self.session.add(data_objs)
        self.session.commit()
        self.session.close()

