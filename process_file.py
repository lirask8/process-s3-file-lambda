from datetime import datetime
from decimal import Decimal


class ProcessFile:
    def __init__(self, original_file_data, has_header=True):
        self.original_file_data = original_file_data
        self.has_header = has_header
        self.file_data = []
        self.transactions = []
        self.read_file()

    def process_rows(self) -> list:
        for i in range(1 if self.has_header else 0, len(self.file_data)):
            transaction_data = self.file_data[i].split(",")
            transaction = {
                "id": transaction_data[0],
                "date": datetime.strptime(transaction_data[1] + "/" + str(datetime.now().year), "%m/%d/%Y"),
                "amount": Decimal(transaction_data[2][1:]),
                "is_credit": True if transaction_data[2][0] == "+" else False
            }
            self.transactions.append(transaction)
        return self.transactions

    def get_summary_data(self):
        summary = {}
        debit_transactions = []
        credit_transactions = []
        month_transactions = {}
        for transaction in self.transactions:
            if transaction["is_credit"]:
                credit_transactions.append(transaction["amount"])
            else:
                debit_transactions.append(transaction["amount"])

            month_str = transaction["date"].strftime("%B")
            if month_str not in month_transactions:
                month_transactions[month_str] = 0
            month_transactions[month_str] += 1

        summary["total_debit"] = sum(debit_transactions)
        summary["total_credit"] = sum(credit_transactions)
        summary["balance"] = summary["total_credit"] - summary["total_debit"]
        summary["debit_avg"] = summary["total_debit"] / len(debit_transactions)
        summary["credit_avg"] = summary["total_credit"] / len(credit_transactions)
        summary["transactions_by_month"] = month_transactions

        return summary

    def read_file(self):
        if self.original_file_data is not None:
            #encoding = chardet.detect(self.original_file_data.getvalue())["encoding"]
            for line in self.original_file_data:
                self.file_data.append(line.decode("utf-8"))