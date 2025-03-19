from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from wordcloud import WordCloud
import sys
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView, QFileDialog
import csv
from io import StringIO

#from PyQt5.QtWidgets import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtChart import QChart, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsTextItem, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QColor, QFont, QBrush, QPainter  # Add QFont import
from PyQt5.QtChart import QLineSeries, QChart, QChartView, QValueAxis, QDateTimeAxis,QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt, QDateTime  # Add Qt import
from DATA225utils import make_connection
from math import cos, sin
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPixmap
from wordcloud import WordCloud
import io
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QSizePolicy
from datetime import datetime
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QValueAxis, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChartView
#from PyQt5.QtWidgets import QStandardItemModel, QStandardItem
# ... other necessary imports ...

 


class TitanicWindowReport(QDialog):
    def __init__(self):
            super().__init__()
            self.ui = uic.loadUi('Report_view_v1.ui')
            
            self.initComboBox()
            self.initComboBox2()
            self.initComboBox3()
            self.initComboBox4()
            self.generateTable()
            
            self.generateTable2()
            #self.generateTable2()
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateTable2)

            self.ui.weekComboBox.currentIndexChanged.connect(self.generateTable)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateTable)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateTable2)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateTable)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateTable2)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateTable)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateTable2)
            self.ui.pushButton.clicked.connect(self.download_table)
            self.ui.pushButton_2.clicked.connect(self.download_table_2)
            #self.ui.comboBox_2.currentIndexChanged.connect(self.generateBarChart)

            #self.ui.comboBox_2.currentIndexChanged.connect(self.generateTable)
            #self.ui.comboBox_2.currentIndexChanged.connect(self.generateTable2)

   
    def initComboBox(self):
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(WEEK(Date)) AS latest_week
            FROM Fulfilment_Dimension_Table
            JOIN Sales_Fact_Table ON Fulfilment_Dimension_Table.Order_ID = Sales_Fact_Table.Order_ID
        """)
        latest_week = cursor.fetchone()[0]
        cursor.execute("""
            SELECT DISTINCT WEEK(Date) AS week
            FROM Fulfilment_Dimension_Table
            JOIN Sales_Fact_Table ON Fulfilment_Dimension_Table.Order_ID = Sales_Fact_Table.Order_ID
            GROUP BY week
        """)
        weeks = [str(row[0]) for row in cursor.fetchall()]
        weeks.insert(0, "All")
        cursor.close()
        conn.close()
        self.ui.weekComboBox.addItems(weeks)
        if latest_week is not None:
            index = self.ui.weekComboBox.findText(str(latest_week))
            if index != -1:
                self.ui.weekComboBox.setCurrentIndex(index)
    def initComboBox2(self):
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        latest_fulfilment = None
        try:
            cursor.execute("""
                SELECT DISTINCT fulfilment 
                FROM Fulfilment_Dimension_Table
            """)
            fulfilments = [str(row[0]) for row in cursor.fetchall()]
            if fulfilments:
                latest_fulfilment = fulfilments[0]
        except Exception as e:
            print("An error occurred:", e)
        finally:
            cursor.close()
            conn.close()
            
        fulfilments.insert(0, "All")
        self.ui.weekComboBox_2.addItems(fulfilments)
        if latest_fulfilment is not None:
            index = self.ui.weekComboBox_2.findText(latest_fulfilment)
            if index != -1:
                self.ui.weekComboBox_2.setCurrentIndex(index)
    def initComboBox3(self):
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        latest_sales_channel = None
        sales_channels = []  # Initialize sales_channels here
        try:
            cursor.execute("""
                SELECT DISTINCT sales_channel 
                FROM Fulfilment_Dimension_Table
            """)
            sales_channels = [str(row[0]) for row in cursor.fetchall()]
            if sales_channels:
                latest_sales_channel = sales_channels[0]
        except Exception as e:
            print("An error occurred:", e)
        finally:
            cursor.close()
            conn.close()

        sales_channels.insert(0, "All")
        self.ui.weekComboBox_3.addItems(sales_channels)
        if latest_sales_channel is not None:
            index = self.ui.weekComboBox_3.findText(latest_sales_channel)
            if index != -1:
                self.ui.weekComboBox_3.setCurrentIndex(index)

    def initComboBox4(self):
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        latest_ship_service_level = None
        try:
            cursor.execute("""
                SELECT DISTINCT ship_service_level 
                FROM Fulfilment_Dimension_Table
            """)
            ship_service_levels = [str(row[0]) for row in cursor.fetchall()]
            if ship_service_levels:
                latest_ship_service_level = ship_service_levels[0]
        except Exception as e:
            print("An error occurred:", e)
        finally:
            cursor.close()
            conn.close()  
            
        ship_service_levels.insert(0, "All")
        self.ui.weekComboBox_4.addItems(ship_service_levels)
        if latest_ship_service_level is not None:
            index = self.ui.weekComboBox_4.findText(latest_ship_service_level)
            if index != -1:
                self.ui.weekComboBox_4.setCurrentIndex(index)
    
    def generateTable(self):
        week_ = self.ui.weekComboBox.currentText()
        fulfilment = self.ui.weekComboBox_2.currentText()
        sales_channel = self.ui.weekComboBox_3.currentText()  # Assuming this is the combo box for sales_channel
        ship_service_level = self.ui.weekComboBox_4.currentText()  # Assuming this is the combo box for ship_service_level
        
        sql_conditions = []
        params = []
        
        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
        if fulfilment != "All":
            sql_conditions.append("fulfilment = %s")
            params.append(fulfilment)
        if sales_channel != "All":  # Condition for sales_channel
            sql_conditions.append("sales_channel = %s")
            params.append(sales_channel)
        if ship_service_level != "All":  # Condition for ship_service_level
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)
        
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT s.Order_id, s.SKU, Date, Size, Color, Category, status, Inventory, Sales_Channel, ship_city, ship_state
        FROM Product_Dimension AS p
        JOIN Sales_Fact_Table AS s ON p.sku = s.sku
        JOIN Fulfilment_Dimension_Table AS f ON f.Order_ID = s.Order_ID
        JOIN Shipping_Fact_Table AS sh ON sh.Order_ID = s.Order_ID
        JOIN Location_Dimension_Table AS l ON l.ship_postal_code = sh.ship_postal_code
        WHERE {where_clause}
        """
        print(sql)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    
        print(len(rows))
    
        cursor.close()
        conn.close()
    
        # Create the model for the QTableView
        model = QStandardItemModel()
    
        headers = ['Order ID', 'SKU', 'Date', 'Size', 'Color', 'Category', 'Shipping Status', 'Inventory', 'Sales Channel', 'Ship City', 'Ship State']
        model.setHorizontalHeaderLabels(headers)
    
        for row_data in rows:
            if None not in row_data:  # Check if the row does not contain null values
                items = [QStandardItem(str(data)) for data in row_data]
                model.appendRow(items)
    
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.verticalHeader().setVisible(False)
    
        self.table_csv_data = StringIO()
        self.table_csvwriter = csv.writer(self.table_csv_data)
    
        # Write headers
        self.table_csvwriter.writerow(headers)
    
        # Write non-null data
        for row_data in rows:
            if None not in row_data:
                self.table_csvwriter.writerow(row_data)

                
    def generateTable2(self):
        week_ = self.ui.weekComboBox.currentText()
        fulfilment = self.ui.weekComboBox_2.currentText()
        sales_channel = self.ui.weekComboBox_3.currentText()  # Assuming this is the combo box for sales_channel
        ship_service_level = self.ui.weekComboBox_4.currentText()  # Assuming this is the combo box for ship_service_level
        
        sql_conditions = []
        params = []
        
        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
        if fulfilment != "All":
            sql_conditions.append("fulfilment = %s")
            params.append(fulfilment)
        if sales_channel != "All":  # Condition for sales_channel
            sql_conditions.append("sales_channel = %s")
            params.append(sales_channel)
        if ship_service_level != "All":  # Condition for ship_service_level
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)
        
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        sql = """
        SELECT s.SKU, Color, Category, Size, SUM(Quantity * Amount) AS Sold_Amount
        FROM Product_Dimension AS p
        JOIN Sales_Fact_Table AS s ON p.sku = s.sku
        JOIN Fulfilment_Dimension_Table AS f ON f.Order_ID = s.Order_ID
        JOIN Shipping_Fact_Table AS sh ON sh.Order_ID = s.Order_ID
        JOIN Location_Dimension_Table AS l ON l.ship_postal_code = sh.ship_postal_code
        WHERE {}
        GROUP BY s.SKU, Color, Category, Size;
        """.format(where_clause)
    
        cursor.execute(sql, params)  # Execute the query with parameters
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    
        # Create the model for the QTableView
        model = QStandardItemModel(self)
        headers = ['SKU', 'Color', 'Category', 'Size', 'Sold Amount']
        model.setHorizontalHeaderLabels(headers)
    
        for row_data in rows:
            items = [QStandardItem(str(data)) for data in row_data]
            model.appendRow(items)
    
        # Update tableView settings
        self.ui.tableView_2.setModel(model)
        self.ui.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_2.resizeColumnsToContents()
        self.ui.tableView_2.verticalHeader().setVisible(False)
    
        # Update CSV data handling
        self.table_2_csv_data = StringIO()
        self.table_2_csvwriter = csv.writer(self.table_2_csv_data)
    
        # Write headers and data to CSV
        self.table_2_csvwriter.writerow(headers)
        self.table_2_csvwriter.writerows(rows)

    
        def createLegend(self):
        #     # Create and return a legend QGraphicsItem
            pass


    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def download_table(self):
        """
        Show this dialog.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, 
                                                   'Save CSV', 
                                                   'output.csv', 
                                                   'CSV Files (*.csv);;All Files (*)')
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csvfile.write(self.table_csv_data.getvalue())
        
        
    def download_table_2(self):
        """
        Show this dialog.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, 
                                                   'Save CSV', 
                                                   'output.csv', 
                                                   'CSV Files (*.csv);;All Files (*)')
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csvfile.write(self.table_2_csv_data.getvalue())
        
     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TitanicWindowReport()
    form.show_dialog()
    sys.exit(app.exec_())
