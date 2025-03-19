from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from wordcloud import WordCloud
import sys
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView

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

 


class TitanicWindowCustomer(QDialog):
    def __init__(self, email):
            super().__init__()
            self.ui = uic.loadUi('customer_view.ui')
            self.currEmail = email
            
            self.initComboBox2()
            # self.initComboBox_3()
            # self.initComboBox_4()
            self.generateBarChart()
            
            self.generateTable()
            self.generateTable2()
            #self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart)

            #self.ui.weekComboBox.currentIndexChanged.connect(self.generateWordCloud)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart)

            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateTable)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateTable2)

    def setcurrEmail(self, email):
        self.currEmail = email

    def initComboBox2(self):
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        latest_order_id = None
        try:
            cursor.execute("""
                SELECT DISTINCT Fulfilment_Dimension_Table.order_id
                FROM Fulfilment_Dimension_Table
                JOIN Sales_Fact_Table ON Fulfilment_Dimension_Table.Order_ID = Sales_Fact_Table.Order_ID
            """)
            order_ids = [str(row[0]) for row in cursor.fetchall()]
            if order_ids:
                latest_order_id = order_ids[0]
        except Exception as e:
            print("An error occurred:", e)
        finally:
            cursor.close()
            conn.close()
        
        conn2 = make_connection(config_file = "techorcas_db.ini")
        cursor2 = conn2.cursor()
        sql = ("""
                select distinct customers_table.OrderID from customers_table 
                where
            """
            
            f"customers_table.Email = '{self.currEmail}' "
            )
        
        
        cursor2.execute(sql)
        rows = cursor2.fetchall()
        cust_orders = []
        cursor2.close()
        conn2.close()
        for row in rows:
            if row[0] in order_ids:
                cust_orders.append(row[0])                
        if cust_orders:
                latest_order_id = cust_orders[0]
        self.ui.weekComboBox_2.addItems(cust_orders)
        if latest_order_id is not None:
            index = self.ui.weekComboBox_2.findText(latest_order_id)
            if index != -1:
                self.ui.weekComboBox_2.setCurrentIndex(index)


    def generateBarChart(self):
        order_id = self.ui.weekComboBox_2.currentText()
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = """
WITH RecentPurchase AS (
    SELECT Product_Dimension.SKU, Size,EXTRACT(MONTH FROM Date) AS PurchaseMonth
    FROM Product_Dimension
    join Sales_Fact_Table on Product_Dimension.sku=Sales_Fact_Table.sku
    WHERE Order_ID = %s
    ORDER BY Date DESC
    LIMIT 1
),
FrequentlyBoughtWith AS (
    SELECT o2.SKU, COUNT(*) AS Frequency
    FROM (    SELECT order_id,Sales_Fact_Table.sku as sku,date,amount,style,color,category,size
    FROM Sales_Fact_Table 
    join Product_Dimension on Product_Dimension.sku=Sales_Fact_Table.sku) o1
    JOIN (    SELECT order_id,Sales_Fact_Table.sku as sku,date,amount,style,color,category,size
    FROM Sales_Fact_Table 
    join Product_Dimension on Product_Dimension.sku=Sales_Fact_Table.sku) o2 ON o1.Order_ID = o2.Order_ID AND o1.SKU != o2.SKU

    WHERE o1.SKU = (SELECT SKU FROM RecentPurchase)
    AND o2.Size = (SELECT Size FROM RecentPurchase)
	AND EXTRACT(MONTH FROM o2.Date) = (SELECT PurchaseMonth FROM RecentPurchase)
    GROUP BY o2.SKU
)
SELECT SKU,Frequency
FROM FrequentlyBoughtWith
ORDER BY Frequency DESC
LIMIT 5;

        """
    
        cursor.execute(sql, (order_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Create a bar series and a QChart
        series = QBarSeries()
        chart = QChart()
        chart.setTitle("Frequently Bought With SKU Frequencies")
    
        # Data for the bar chart
        skus = [row[0] for row in rows]
        frequencies = [row[1] for row in rows]
        bar_set = QBarSet('Frequency')
        bar_set.append(frequencies)
        series.append(bar_set)
    
        chart.addSeries(series)
    
        # Create axes
        axisX = QBarCategoryAxis()
        axisX.append(skus)
    
        # Adjust label font size
        font = QFont()
        font.setPointSize(7)  # Set the point size to be smaller
        axisX.setLabelsFont(font)
    
        # Rotate labels to fit
        axisX.setLabelsAngle(-45)  # Rotate labels by -45 degrees
    
        axisY = QValueAxis()
        max_frequency = max(frequencies) if frequencies else 0
        axisY.setRange(0, max_frequency)
    
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
    
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
    
        # Set the chart in the QChartView
        self.ui.graphicsView_2.setChart(chart)
        self.ui.graphicsView_2.setRenderHint(QPainter.Antialiasing)
 

    # ... (other parts of your TitanicWindowCustomer class)
    

    
    
    def generateTable(self):
        order_id = self.ui.weekComboBox_2.currentText()
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = """
        SELECT Fulfilment_Dimension_Table.Order_ID, Product_Dimension.SKU, Date, Size, Color, Category, status as Shipping_Status,
        Quantity*Amount as TotalAmount, ship_city
        FROM Product_Dimension
        JOIN Sales_Fact_Table ON Product_Dimension.sku = Sales_Fact_Table.sku
        JOIN Fulfilment_Dimension_Table ON Fulfilment_Dimension_Table.Order_ID = Sales_Fact_Table.Order_ID
        JOIN Shipping_Fact_Table ON Shipping_Fact_Table.Order_ID = Sales_Fact_Table.Order_ID
        JOIN Location_Dimension_Table ON Location_Dimension_Table.ship_postal_code = Shipping_Fact_Table.ship_postal_code
        where Fulfilment_Dimension_Table.Order_ID=%s
        ORDER BY Date DESC
        """
    
        cursor.execute(sql, (order_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    
        # Create the model for the QTableView
        model = QStandardItemModel()
    
        # Assuming all rows have the same number of columns
        headers = ['Order ID', 'SKU', 'Date', 'Size', 'Color', 'Category', 'Shipping Status', 'Total Amount', 'Ship City']
    
        # Set the number of rows in the model
        model.setRowCount(len(headers))
        # Set the number of columns in the model
        model.setColumnCount(len(rows) + 1)  # +1 for the header column
    
        # Populate the header row
        for i, header in enumerate(headers):
            item = QStandardItem(header)
            model.setItem(i, 0, item)  # Set the header in the first column
    
        # Populate the data
        for col, row_data in enumerate(rows, 1):  # Start at column 1 to leave space for headers
            for row, data in enumerate(row_data):
                item = QStandardItem(str(data))
                model.setItem(row, col, item)
    
    # Assuming self.ui.tableView is your QTableView
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.resizeColumnsToContents()
    
        # If you want to hide the vertical header (the row numbers):
        self.ui.tableView.verticalHeader().setVisible(False)
    
        # If you want to hide the horizontal header (the column numbers):
        self.ui.tableView.horizontalHeader().setVisible(False)
            
            
    def generateTable2(self):
        order_id = self.ui.weekComboBox_2.currentText()
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = """
        WITH RecentPurchase AS (
    SELECT Product_Dimension.SKU, Size, EXTRACT(MONTH FROM Date) AS PurchaseMonth
    FROM Product_Dimension
    JOIN Sales_Fact_Table ON Product_Dimension.sku = Sales_Fact_Table.sku
    WHERE Order_ID = %s
    ORDER BY Date DESC
    LIMIT 1
),
FrequentlyBoughtWith AS (
    SELECT o2.SKU, COUNT(*) AS Frequency
    FROM (   SELECT order_id,Sales_Fact_Table.sku as sku,date,amount,style,color,category,size
    FROM Sales_Fact_Table 
    join Product_Dimension on Product_Dimension.sku=Sales_Fact_Table.sku) AS o1
    JOIN (   SELECT order_id,Sales_Fact_Table.sku as sku,date,amount,style,color,category,size
    FROM Sales_Fact_Table 
    join Product_Dimension on Product_Dimension.sku=Sales_Fact_Table.sku)
    AS o2 ON o1.Order_ID = o2.Order_ID AND o1.SKU != o2.SKU
    JOIN Product_Dimension ON Product_Dimension.sku = o1.sku
    WHERE o1.SKU = (SELECT SKU FROM RecentPurchase)
    AND o2.Size = (SELECT Size FROM RecentPurchase)
    AND EXTRACT(MONTH FROM o2.Date) = (SELECT PurchaseMonth FROM RecentPurchase)
    GROUP BY o2.SKU
    ORDER BY Frequency DESC
    LIMIT 5
)
SELECT distinct p.SKU, s.Date, p.Size, p.Color, p.Category,
       Quantity * s.Amount as TotalAmount
FROM Product_Dimension AS p
JOIN Sales_Fact_Table AS s ON p.sku = s.sku
JOIN Fulfilment_Dimension_Table AS f ON f.Order_ID = s.Order_ID
JOIN Shipping_Fact_Table AS sh ON sh.Order_ID = s.Order_ID
JOIN Location_Dimension_Table AS l ON l.ship_postal_code = sh.ship_postal_code
JOIN FrequentlyBoughtWith AS fbw ON fbw.SKU = p.SKU
-- where f.order_id = '171-9918163-5396330'
ORDER BY s.Date DESC
limit 5

        """
    
        cursor.execute(sql, (order_id,))  # Use parameterized execution to prevent SQL injection
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    
        # Create the model for the QTableView
        model = QStandardItemModel(self)
        headers = ['SKU', 'Size', 'Color', 'Category', 'Total Amount']
        model.setHorizontalHeaderLabels(headers)
    
        for row_data in rows:
            # Exclude the date from the displayed data
            items = [QStandardItem(str(data)) for i, data in enumerate(row_data) if i != 1]  # Skip index 1 (Date)
            model.appendRow(items)

    
        # Replace 'tableView' with the actual name of your QTableView in the UI file
        self.ui.tableView_2.setModel(model)
        self.ui.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_2.resizeColumnsToContents()
    
        # Optionally, hide the vertical header if you do not want to show row numbers
        self.ui.tableView_2.verticalHeader().setVisible(False)
    
            

    
    
        def createLegend(self):
        #     # Create and return a legend QGraphicsItem
            pass


 


    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TitanicWindowCustomer("ketan@gmail.com")
    form.show_dialog()
    sys.exit(app.exec_())
