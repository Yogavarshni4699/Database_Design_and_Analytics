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
from TitanicWindowDD import TitanicWindowDD


# ... other necessary imports ...

 


class TitanicWindow(QDialog):
    def __init__(self):
            super().__init__()
            self.ui = uic.loadUi('order_view.ui')
            self.initComboBox()
            self.initComboBox2()
            self.initComboBox3()
            self.initComboBox4()
            self.generateBarChart()
            self.generatePieChart()
            self.generateBarChart2()
            self.generateWordCloud()
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart)
            self.ui.weekComboBox.currentIndexChanged.connect(self.generatePieChart)
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox.currentIndexChanged.connect(self.generateWordCloud)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generatePieChart)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_2.currentIndexChanged.connect(self.generateWordCloud)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateBarChart)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generatePieChart)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_3.currentIndexChanged.connect(self.generateWordCloud)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateBarChart)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generatePieChart)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateBarChart2)
            self.ui.weekComboBox_4.currentIndexChanged.connect(self.generateWordCloud)
            self.drilldown_dialog = TitanicWindowDD()
            self.ui.commandLinkButton.clicked.connect(
                self.show_drilldown_dialog)
            
    def show_drilldown_dialog(self):
        self.drilldown_dialog.show_dialog()
            
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


    def generateBarChart(self):
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

        
        print(where_clause)
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT Date,
            COUNT(DISTINCT Fulfilment_Dimension_Table.Order_ID) AS Orders_Count,
            COUNT(DISTINCT Sales_Fact_Table.sku) AS sku_Count
        FROM Fulfilment_Dimension_Table
            join Sales_Fact_Table on Fulfilment_Dimension_Table.Order_ID=Sales_Fact_Table.Order_ID
        WHERE {where_clause}
        GROUP BY Date
        ORDER BY Date
        """
        print(sql)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    
        cursor.close()
        conn.close()
    
        series_orders = QLineSeries(name="Orders Count")
        series_sku = QLineSeries(name="SKU Count")
        
        max_value = 0
    
        for row in rows:
            # Combine the date object with a time component to create a datetime object
            date_time = datetime.combine(row[0], datetime.min.time())  # Assuming row[0] is a date object
            qdate = QDateTime(date_time)
            series_orders.append(qdate.toMSecsSinceEpoch(), row[1])
            series_sku.append(qdate.toMSecsSinceEpoch(), row[2])
            max_value = max(max_value, max(row[1], row[2]))
            
        # Connect the hovered signal for series_orders
        series_orders.hovered.connect(lambda point, state: self.showLineSeriesTooltip(point, state, "Orders Count"))

        # Connect the hovered signal for series_sku
        series_sku.hovered.connect(lambda point, state: self.showLineSeriesTooltip(point, state, "SKU Count"))

        chart = QChart()
        chart.addSeries(series_orders)
        chart.addSeries(series_sku)
        chart.setTitle("Orders and SKU Counts Over Time")
    
        axisX = QDateTimeAxis()
        axisX.setFormat("yyyy-MM-dd")
        axisX.setTitleText("Date")
        chart.addAxis(axisX, Qt.AlignBottom)
    
        axisY = QValueAxis()
        axisY.setTitleText("Count")
        axisY.setRange(0, max_value)
        chart.addAxis(axisY, Qt.AlignLeft)
    
        series_orders.attachAxis(axisX)
        series_orders.attachAxis(axisY)
        series_sku.attachAxis(axisX)
        series_sku.attachAxis(axisY)
    
        self.ui.graphicsView.setChart(chart)
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)
        
                   
        # Connect the hovered signal for series_orders
        series_orders.hovered.connect(lambda point, state: self.showLineSeriesTooltip(point, state, "Orders Count"))

        # Connect the hovered signal for series_sku
        series_sku.hovered.connect(lambda point, state: self.showLineSeriesTooltip(point, state, "SKU Count"))
        
    
    def showLineSeriesTooltip(self, point, state, series_name):
        if state:  # If the point is hovered
            tooltip_text = f"{series_name} Count: {point.y()}"
            QToolTip.showText(QCursor.pos(), tooltip_text)
        else:
            QToolTip.hideText()

    
    def generatePieChart(self):
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

        
        print(where_clause)
        
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
        
        sql = f"""
        select status, count(Sales_Fact_Table.order_id) as order_count 
        from Fulfilment_Dimension_Table
        join Sales_Fact_Table on Sales_Fact_Table.order_id=Fulfilment_Dimension_Table.order_id
        WHERE {where_clause}
        group by status
        """
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    
        cursor.close()
        conn.close()
        
        # Create the pie series
        series = QPieSeries()
        total_orders = sum(row[1] for row in rows)
        
        for row in rows:
            status = row[0]
            order_count = row[1]
            slice = QPieSlice(f"{status} ({order_count})", order_count)
            series.append(slice)
            # Set color based on status
            # Assuming you have a method getStatusColor() that returns a QColor for a given status
            slice.setColor(self.getStatusColor(status))
            slice.hovered.connect(lambda state, s=slice: self.showPieSliceTooltip(state, s))
    
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Status Division")
        
        legend = chart.legend()
        legend.setVisible(True)
        legend.setAlignment(Qt.AlignRight)  # Adjust legend position
        #legend.setMarkerShape(QLegend.MarkerShapeRectangle)  # Choose your preferred shape
    
        # Customize legend font size (optional)
        font = legend.font()
        font.setPointSize(8)  # Adjust the point size as needed
        legend.setFont(font)
    
        # Customize legend icon size (optional)
        #legend.setIconSize(QSize(10, 10))  # Adjust width and height as needed
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # Smooth the pie chart
    
        # Set the chart in the QGraphicsView
        self.ui.graphicsView_2.setChart(chart)
        self.ui.graphicsView_2.setRenderHint(QPainter.Antialiasing)  # Smooth the lines
    
    
    def showPieSliceTooltip(self, state, slice):
        if state:  # If the slice is hovered
            QToolTip.showText(QCursor.pos(), slice.label())
        else:
            QToolTip.hideText()


    def getStatusColor(self, status):
        # Define colors for different statuses
        colors = {
            'Cancelled': QColor(255, 102, 102),  # Soft Red
            'Shipped - Delivered to Buyer': QColor(102, 178, 255),  # Soft Blue
            'Shipped': QColor(80, 200, 120),  # Soft Green
            'Shipped - Returned to Seller': QColor(0, 128, 0),  # Darker Green
            'Shipped - Rejected by Buyer': QColor(192, 192, 192),  # Light Gray
            'Shipped - Lost in Transit': QColor(255, 255, 102),  # Soft Yellow
            'Shipped - Out for Delivery': QColor(255, 153, 255),  # Soft Magenta
            'Shipped - Returning to Seller': QColor(153, 204, 255),  # Soft Cyan
            'Shipped - Picked Up': QColor(51, 102, 255),  # Soft Dark Blue
            'Pending': QColor(255, 204, 153),  # Soft Orange
            'Pending - Waiting for Pick Up': QColor(255, 229, 153),  # Soft Gold
            'Shipped - Damaged': QColor(204, 0, 0),  # Darker Red
            'Shipping': QColor(255, 178, 102)  # Soft Dark Orange
        }

        return colors.get(status, QColor(Qt.gray)) # Default color

    # ... [Rest of your TitanicWindow class]

# ... [Rest of your Python script]




    
    
    def generateBarChart2(self):
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
        if sales_channel != "All":
            sql_conditions.append("sales_channel = %s")
            params.append(sales_channel)
        if ship_service_level != "All":
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)
    
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT  Category,COUNT(f.Order_ID) as Order_Count
        FROM Product_Dimension AS p
        JOIN Sales_Fact_Table AS s ON p.sku = s.sku
        JOIN Fulfilment_Dimension_Table AS f ON f.Order_ID = s.Order_ID
        JOIN Shipping_Fact_Table AS sh ON sh.Order_ID = s.Order_ID
        JOIN Location_Dimension_Table AS l ON l.ship_postal_code = sh.ship_postal_code
        WHERE {where_clause}
        GROUP BY Category
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
        categories = [row[0] for row in rows]
        order_counts = [row[1] for row in rows]
        bar_set = QBarSet('Order Count')
        bar_set.append(order_counts)
        bar_set.hovered.connect(lambda status, index, 
            bar_set=bar_set: self.showBarTooltip(status, index, bar_set))
        series.append(bar_set)
        
    
        chart.addSeries(series)
    
        # Create axes
        axisX = QBarCategoryAxis()
        axisX.append(categories)
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
        self.ui.graphicsView_3.setChart(chart)
        self.ui.graphicsView_3.setRenderHint(QPainter.Antialiasing)  


    def showBarTooltip(self, status, index, bar_set):
        if status:  # If hovered
            value = bar_set.at(index)
            QToolTip.showText(QCursor.pos(), f"Count: {value}")
        else:
            QToolTip.hideText()


    def createLegend(self):
    #     # Create and return a legend QGraphicsItem
        pass


    def generateWordCloud(self):
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
        if sales_channel != "All":
            sql_conditions.append("sales_channel = %s")
            params.append(sales_channel)
        if ship_service_level != "All":
            sql_conditions.append("ship_service_level = %s")
            params.append(ship_service_level)
    
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
    
        conn = make_connection(config_file='techorcas_wh.ini')
        cursor = conn.cursor()
    
        sql = f"""
        SELECT ship_state, COUNT(Fulfilment_Dimension_Table.Order_ID) as Order_Count
        FROM Sales_Fact_Table
        JOIN Fulfilment_Dimension_Table on Fulfilment_Dimension_Table.Order_ID=Sales_Fact_Table.Order_ID
        JOIN Shipping_Fact_Table on Sales_Fact_Table.order_id=Shipping_Fact_Table.order_id
        JOIN Location_Dimension_Table on Location_Dimension_Table.ship_postal_code=Shipping_Fact_Table.ship_postal_code
        WHERE {where_clause}
        GROUP BY ship_state
        """
    
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    
        cursor.close()
        conn.close()
        
        # Create a dictionary for the word cloud where the keys are states and the values are order counts
        wordcloud_data = {row[0]: row[1] for row in rows}
        
        # Generate the word cloud image
        wc = WordCloud(width=800, height=400, background_color='white')
        wc.generate_from_frequencies(wordcloud_data)
        
        # Convert the word cloud image to QPixmap
        wordcloud_image = wc.to_image()
        byte_array = io.BytesIO()
        wordcloud_image.save(byte_array, format='PNG')
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.getvalue())
        
        # Display the QPixmap in the QGraphicsView
        scene = QGraphicsScene(self)
        scene.addPixmap(pixmap)
        self.ui.graphicsView_4.setScene(scene)
        self.ui.graphicsView_4.show()
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TitanicWindow()
    form.show_dialog()
    sys.exit(app.exec_())
