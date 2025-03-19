from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from wordcloud import WordCloud

from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
import sys
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
#from PyQt5.QtWidgets import QLegend
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QToolTip


class TitanicWindowDD(QDialog):
    def __init__(self):
            super().__init__()
            self.ui = uic.loadUi('Drill_view.ui')
            self.initComboBox()
            self.initComboBox2()
            self.initComboBox_3()
            self.initComboBox_4()
            self.initComboBox_5()

            self.generateBarChart2()
            self.generateBarChart3()
            self.generateBarChart4()
            self.generateBarChart5()


            self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart3)
            self.ui.weekComboBox.currentIndexChanged.connect(self.initComboBox_3)
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart4)
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart5)

            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart3)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart4)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart5)
            
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateBarChart3)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateBarChart4)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateBarChart5)
            
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateBarChart3)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateBarChart4)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateBarChart5)
            
            self.ui.weekComboBox_5.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_5.currentIndexChanged.connect(self.generateBarChart3)
            self.ui.weekComboBox_5.currentIndexChanged.connect(self.generateBarChart4)
            self.ui.weekComboBox_5.currentIndexChanged.connect(self.generateBarChart5)

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
    def initComboBox_3(self):
        week_ = self.ui.weekComboBox.currentText()
        print("Week selected: " + week_)
        sql_conditions = []
        params = []

        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
            
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
            
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        fulfilments = []  # Initialize fulfilments here
        latest_fulfilment = None
        
        sql = f"""
        SELECT DISTINCT (Date) AS Date
        FROM Fulfilment_Dimension_Table
        JOIN Sales_Fact_Table ON Fulfilment_Dimension_Table.Order_ID = Sales_Fact_Table.Order_ID
        where {where_clause}
        """
    
        try:
            cursor.execute(sql, params)
            
            fulfilments = [str(row[0]) for row in cursor.fetchall()]
            if fulfilments:
                latest_fulfilment = fulfilments[0]
        except Exception as e:
            print("An error occurred:", e)
        finally:
            cursor.close()
            conn.close()
        
        fulfilments.insert(0, "All") 
        # Ensure this is outside of the try-except block
        self.ui.weekComboBox_3.clear()
        self.ui.weekComboBox_3.addItems(fulfilments)
        if latest_fulfilment is not None:
            index = self.ui.weekComboBox_3.findText(latest_fulfilment)
            if index != -1:
                self.ui.weekComboBox_3.setCurrentIndex(index)

    def initComboBox_4(self):
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        latest_sales_channel = None
        
        try:
            cursor.execute("""
                SELECT DISTINCT Sales_Channel
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
        self.ui.weekComboBox_4.addItems(sales_channels)
    
        if latest_sales_channel is not None:
            index = self.ui.weekComboBox_4.findText(latest_sales_channel)
            if index != -1:
                self.ui.weekComboBox_4.setCurrentIndex(index)
                
    def initComboBox_5(self):
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
        self.ui.weekComboBox_5.addItems(ship_service_levels)
    
        if latest_ship_service_level is not None:
            index = self.ui.weekComboBox_5.findText(latest_ship_service_level)
            if index != -1:
                self.ui.weekComboBox_5.setCurrentIndex(index)




    
    def generateBarChart2(self):
        week_ = self.ui.weekComboBox.currentText()
        fulfilment = self.ui.weekComboBox_2.currentText()
        Date = self.ui.weekComboBox_3.currentText()
        Sales_Channel = self.ui.weekComboBox_4.currentText()
        ship_service_level = self.ui.weekComboBox_5.currentText()
        
        sql_conditions = []
        params = []

        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
        if fulfilment != "All":
            sql_conditions.append("fulfilment = %s")
            params.append(fulfilment)
        if Date != "All":
            sql_conditions.append("Date = %s")
            params.append(Date)
        if Sales_Channel != "All":
            sql_conditions.append("Sales_Channel = %s")
            params.append(Sales_Channel)
        if ship_service_level != "All":
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)            

        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
        
        print(where_clause)
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT category, COUNT(Sales_Fact_Table.Order_ID) as Order_Count
        FROM Sales_Fact_Table
        JOIN Product_Dimension on Product_Dimension.sku=Sales_Fact_Table.sku
        JOIN Fulfilment_Dimension_Table on Fulfilment_Dimension_Table.Order_ID=Sales_Fact_Table.Order_ID
        WHERE {where_clause}
        GROUP BY category
        """
    
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    
        cursor.close()
        conn.close()
    
        # Create a bar series and a QChart
        series = QBarSeries()
        chart = QChart()
        chart.setTitle("Category-wise Order Count")
    
        # The categories (x-axis labels)
        self.categories = [row[0] for row in rows]
        order_counts = [row[1] for row in rows]
        bar_set = QBarSet('Order Count')
        bar_set.append(order_counts)
        bar_set.hovered.connect(lambda status, index, 
            bar_set=bar_set: self.showBarTooltip(status, index, bar_set))
        bar_set.clicked.connect(lambda index, 
            bar_set=bar_set: self.filterSKUChart(index, bar_set))
        bar_set.clicked.connect(lambda index, 
            bar_set=bar_set: self.filterCityChart(index, bar_set))
        bar_set.clicked.connect(lambda index, 
            bar_set=bar_set: self.filterSKUCityChart(index, bar_set))
        series.append(bar_set)
        
    
        chart.addSeries(series)
    
        # Create axes
        axisX = QBarCategoryAxis()
        axisX.append(self.categories)
        axisX.setLabelsAngle(-90)
        axisY = QValueAxis()
        max_order_count = max(order_counts) if order_counts else 0
        axisY.setRange(0, max_order_count)  # Y-axis range
    
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
    
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
    
        # Assuming self.ui.graphicsView_3 is a QChartView
        self.ui.graphicsView.setChart(chart)
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)  
        
    def filterSKUChart(self, index, bar_set):
        # Get the category name based on the clicked bar index
        category = self.categories[index]
        print("Category: "+ category)
        self.generateBar3WithCategory(category)
        
    def filterCityChart(self, index, bar_set):
        # Get the category name based on the clicked bar index
        category = self.categories[index]
        print("Category: "+ category)
        self.generateBar4WithCategory(category, None)
        
    def filterCityChartFromSku(self, index, bar_set):
        # Get the category name based on the clicked bar index
        sku = self.skus[index]
        print("Sku: "+ sku)
        self.generateBar4WithCategory(None, sku)
        
    def filterSKUCityChart(self, index, bar_set):
        # Get the category name based on the clicked bar index
        category = self.categories[index]
        print("Category: "+ category)
        self.generateBar5WithCategory(category)


    def generateBar3WithCategory(self, category):
        print("Category sent" + str(category))
        week_ = self.ui.weekComboBox.currentText()
        fulfilment = self.ui.weekComboBox_2.currentText()
        Date = self.ui.weekComboBox_3.currentText()
        Sales_Channel = self.ui.weekComboBox_4.currentText()
        ship_service_level = self.ui.weekComboBox_5.currentText()
        
        sql_conditions = []
        params = []

        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
        if fulfilment != "All":
            sql_conditions.append("fulfilment = %s")
            params.append(fulfilment)
        if Date != "All":
            sql_conditions.append("Date = %s")
            params.append(Date)
        if category != None:
            sql_conditions.append("Category = %s")
            params.append(category)
        if Sales_Channel != "All":
            sql_conditions.append("Sales_Channel = %s")
            params.append(Sales_Channel)
        if ship_service_level != "All":
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)            

        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
        
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT Product_Dimension.sku, COUNT(Sales_Fact_Table.Order_ID) as Order_Count
        FROM Sales_Fact_Table
        JOIN Product_Dimension on Product_Dimension.sku=Sales_Fact_Table.sku
        JOIN Fulfilment_Dimension_Table on Fulfilment_Dimension_Table.Order_ID=Sales_Fact_Table.Order_ID
        WHERE {where_clause}
        GROUP BY sku
        """
    
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    
        series = QBarSeries()
        chart = QChart()
        chart.setTitle("SKU-wise Order Count")

        self.skus = [row[0] for row in rows]
        order_counts = [row[1] for row in rows]
        bar_set = QBarSet('Order Count')
        bar_set.append(order_counts)
        bar_set.hovered.connect(lambda status, index, 
            bar_set=bar_set: self.showBarTooltipSKU(status, index, bar_set))
        bar_set.clicked.connect(lambda index, 
            bar_set=bar_set: self.filterCityChartFromSku(index, bar_set))

        series.append(bar_set)
    
        chart.addSeries(series)
    
        axisX = QBarCategoryAxis()
        axisX.append(self.skus)
        axisX.setLabelsAngle(-90)  # Rotate labels for better readability
        axisY = QValueAxis()
        max_order_count = max(order_counts) if order_counts else 0
        axisY.setRange(0, max_order_count)
    
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
    
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
    
        self.ui.graphicsView_2.setChart(chart)
        self.ui.graphicsView_2.setRenderHint(QPainter.Antialiasing)
    
    def generateBar4WithCategory(self, category=None, sku=None):
        week_ = self.ui.weekComboBox.currentText()
        fulfilment = self.ui.weekComboBox_2.currentText()
        Date = self.ui.weekComboBox_3.currentText()
        Sales_Channel = self.ui.weekComboBox_4.currentText()
        ship_service_level = self.ui.weekComboBox_5.currentText()
        
        
        sql_conditions = []
        params = []
    
        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
        if fulfilment != "All":
            sql_conditions.append("fulfilment = %s")
            params.append(fulfilment)
        if Date != "All":
            sql_conditions.append("Date = %s")
            params.append(Date)
        if category != None:
            sql_conditions.append("Category = %s")
            params.append(category)
        if sku != None:
            sql_conditions.append("p.sku = %s")
            params.append(sku)
        if Sales_Channel != "All":
            sql_conditions.append("Sales_Channel = %s")
            params.append(Sales_Channel)
        if ship_service_level != "All":
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)            

            
    
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
        
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT distinct l.ship_city, COUNT(s.Order_ID) as Order_Count
        FROM Product_Dimension AS p
        JOIN Sales_Fact_Table AS s ON p.sku = s.sku
        JOIN Fulfilment_Dimension_Table AS f ON f.Order_ID = s.Order_ID
        JOIN Shipping_Fact_Table AS sh ON sh.Order_ID = s.Order_ID
        JOIN Location_Dimension_Table AS l ON l.ship_postal_code = sh.ship_postal_code
        WHERE {where_clause}
        GROUP BY l.ship_city
        """
    
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    
        series = QBarSeries()
        chart = QChart()
        chart.setTitle("City-wise Order Count")
    
        cities = [row[0] for row in rows]
        order_counts = [row[1] for row in rows]
        bar_set = QBarSet('Order Count')
        bar_set.append(order_counts)
        bar_set.hovered.connect(lambda status, index, 
            bar_set=bar_set: self.showBarTooltip(status, index, bar_set))
    
        series.append(bar_set)
    
        chart.addSeries(series)
    
        axisX = QBarCategoryAxis()
        axisX.append(cities)
        axisX.setLabelsAngle(-90)  # Rotate labels for better readability
        axisY = QValueAxis()
        max_order_count = max(order_counts) if order_counts else 0
        axisY.setRange(0, max_order_count)
    
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
    
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
    
        self.ui.graphicsView_3.setChart(chart)
        self.ui.graphicsView_3.setRenderHint(QPainter.Antialiasing)
    
    
        # ... [rest of your TitanicWindowDD class]
    def generateBar5WithCategory(self, category=None):
        week_ = self.ui.weekComboBox.currentText()
        fulfilment = self.ui.weekComboBox_2.currentText()
        Date = self.ui.weekComboBox_3.currentText()
        Sales_Channel = self.ui.weekComboBox_4.currentText()
        ship_service_level = self.ui.weekComboBox_5.currentText()
        
        
        sql_conditions = []
        params = []
    
        if week_ != "All":
            sql_conditions.append("WEEK(Date) = %s")
            params.append(int(week_))
        if fulfilment != "All":
            sql_conditions.append("fulfilment = %s")
            params.append(fulfilment)
        if Date != "All":
            sql_conditions.append("Date = %s")
            params.append(Date)
        if category != None:
            sql_conditions.append("Category = %s")
            params.append(category)
        if Sales_Channel != "All":
            sql_conditions.append("Sales_Channel = %s")
            params.append(Sales_Channel)
        if ship_service_level != "All":
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)            

            
    
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
        
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
    SELECT distinct s.SKU,COUNT(s.inventory) as Order_Inventory
    FROM Product_Dimension AS p
    JOIN Sales_Fact_Table AS s ON p.sku = s.sku
    JOIN Fulfilment_Dimension_Table AS f ON f.Order_ID = s.Order_ID
    JOIN Shipping_Fact_Table AS sh ON sh.Order_ID = s.Order_ID
    JOIN Location_Dimension_Table AS l ON l.ship_postal_code = sh.ship_postal_code
    WHERE {where_clause}
	group by s.SKU;
        """
    
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    
        series = QBarSeries()
        chart = QChart()
        chart.setTitle("SKU-wise Inventory Count")
    
        cities = [row[0] for row in rows]
        order_counts = [row[1] for row in rows]
        bar_set = QBarSet('Order Count')
        bar_set.append(order_counts)
        bar_set.hovered.connect(lambda status, index, 
            bar_set=bar_set: self.showBarTooltip(status, index, bar_set))
    
        series.append(bar_set)
    
        chart.addSeries(series)
    
        axisX = QBarCategoryAxis()
        axisX.append(cities)
        axisX.setLabelsAngle(-90)  # Rotate labels for better readability
        axisY = QValueAxis()
        max_order_count = max(order_counts) if order_counts else 0
        axisY.setRange(0, max_order_count)
    
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
    
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
    
        self.ui.graphicsView_4.setChart(chart)
        self.ui.graphicsView_4.setRenderHint(QPainter.Antialiasing)
    
    

        
    def generateBarChart3(self):
        self.generateBar3WithCategory(None)
        
    def generateBarChart4(self):
        self.generateBar4WithCategory(None)
        
    def generateBarChart5(self):
        self.generateBar5WithCategory(None) 
        

    # ... [rest of your TitanicWindowDD class]

        


    def showBarTooltip(self, status, index, bar_set):
        if status:  # If hovered
            value = bar_set.at(index)
            QToolTip.showText(QCursor.pos(), f"Count: {value}")
        else:
            QToolTip.hideText()
            
    def showBarTooltipSKU(self, status, index, bar_set):
        if status:  # If hovered
            value = bar_set.at(index)
            sku = self.skus[index]
            QToolTip.showText(QCursor.pos(), f"Sku: {sku} Count: {value}")
        else:
            QToolTip.hideText()


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
    form = TitanicWindowDD()
    form.show_dialog()
    sys.exit(app.exec_())
