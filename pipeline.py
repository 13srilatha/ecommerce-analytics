import psycopg2
import pandas as pd
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analytics_pipeline.log'),
        logging.StreamHandler()
    ]
)

class AnalyticsPipeline:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            logging.info("✅ Connected to database successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Database connection failed: {e}")
            return False
    
    def run_query(self, query_name, query):
        try:
            df = pd.read_sql_query(query, self.conn)
            logging.info(f"✅ {query_name} executed. Rows: {len(df)}")
            return df
        except Exception as e:
            logging.error(f"❌ {query_name} failed: {e}")
            return None
    
    def validate_data(self, df, query_name):
        try:
            if df.empty:
                logging.warning(f"⚠️  {query_name}: Empty result set")
                return False
            
            null_count = df.isnull().sum().sum()
            if null_count > 0:
                logging.warning(f"⚠️  {query_name}: Found {null_count} NULL values")
            
            logging.info(f"✅ {query_name}: Data validation passed")
            return True
        except Exception as e:
            logging.error(f"❌ Data validation failed: {e}")
            return False
    
    def generate_report(self):
        report = {}
        
        query1 = """
        SELECT 
            p.product_name,
            p.category,
            COUNT(o.order_id) as order_count,
            SUM(o.total_amount) as total_revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value
        FROM products p
        LEFT JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_revenue DESC;
        """
        df1 = self.run_query("Query 1: Revenue by Product", query1)
        if df1 is not None and self.validate_data(df1, "Query 1"):
            report['revenue_by_product'] = df1
        
        query2 = """
        SELECT 
            c.customer_id,
            c.customer_name,
            c.region,
            COUNT(o.order_id) as order_count,
            SUM(o.total_amount) as total_spent,
            ROUND(AVG(o.total_amount), 2) as avg_order_value
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name, c.region
        ORDER BY total_spent DESC
        LIMIT 5;
        """
        df2 = self.run_query("Query 2: Top 5 Customers", query2)
        if df2 is not None and self.validate_data(df2, "Query 2"):
            report['top_customers'] = df2
        
        query3 = """
        SELECT 
            c.region,
            COUNT(DISTINCT c.customer_id) as customer_count,
            COUNT(o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.region
        ORDER BY total_revenue DESC;
        """
        df3 = self.run_query("Query 3: Revenue by Region", query3)
        if df3 is not None and self.validate_data(df3, "Query 3"):
            report['revenue_by_region'] = df3
        
        query4 = """
        SELECT 
            status,
            COUNT(*) as order_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage,
            SUM(total_amount) as total_amount
        FROM orders
        GROUP BY status
        ORDER BY order_count DESC;
        """
        df4 = self.run_query("Query 4: Order Status Breakdown", query4)
        if df4 is not None and self.validate_data(df4, "Query 4"):
            report['order_status'] = df4
        
        query5 = """
        SELECT 
            order_date,
            COUNT(order_id) as orders,
            SUM(total_amount) as revenue,
            ROUND(AVG(total_amount), 2) as avg_order_value
        FROM orders
        GROUP BY order_date
        ORDER BY order_date;
        """
        df5 = self.run_query("Query 5: Revenue Trend", query5)
        if df5 is not None and self.validate_data(df5, "Query 5"):
            report['revenue_trend'] = df5
        
        query6 = """
        SELECT 
            c.customer_id,
            c.customer_name,
            SUM(o.total_amount) as total_spent
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spent DESC
        LIMIT 3;
        """
        df6 = self.run_query("Query 6: Pareto Analysis", query6)
        if df6 is not None and self.validate_data(df6, "Query 6"):
            report['pareto_analysis'] = df6
        
        query7 = """
        SELECT 
            CASE 
                WHEN order_count = 1 THEN 'One-Time Buyer'
                ELSE 'Repeat Customer'
            END as customer_type,
            COUNT(*) as customer_count,
            ROUND(AVG(total_spent), 2) as avg_customer_value
        FROM (
            SELECT 
                c.customer_id,
                COUNT(o.order_id) as order_count,
                SUM(o.total_amount) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
        ) subquery
        GROUP BY customer_type;
        """
        df7 = self.run_query("Query 7: Repeat vs One-Time", query7)
        if df7 is not None and self.validate_data(df7, "Query 7"):
            report['repeat_vs_onetime'] = df7
        
        query8 = """
        SELECT 
            product_id,
            product_name,
            category,
            stock,
            price,
            price * stock as inventory_value
        FROM products
        WHERE stock < 20
        ORDER BY stock ASC;
        """
        df8 = self.run_query("Query 8: Low Stock", query8)
        if df8 is not None and self.validate_data(df8, "Query 8"):
            report['low_stock'] = df8
        
        query9 = """
        SELECT 
            CASE 
                WHEN lifetime_value > 50000 THEN 'Premium'
                WHEN lifetime_value > 30000 THEN 'Standard'
                ELSE 'Basic'
            END as customer_segment,
            COUNT(*) as customer_count,
            ROUND(AVG(lifetime_value), 2) as avg_ltv,
            SUM(lifetime_value) as total_ltv
        FROM customers
        GROUP BY customer_segment
        ORDER BY total_ltv DESC;
        """
        df9 = self.run_query("Query 9: LTV Segments", query9)
        if df9 is not None and self.validate_data(df9, "Query 9"):
            report['ltv_segments'] = df9
        
        query10 = """
        SELECT 
            p.category,
            COUNT(DISTINCT p.product_id) as product_count,
            COUNT(o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue
        FROM products p
        LEFT JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """
        df10 = self.run_query("Query 10: Category Performance", query10)
        if df10 is not None and self.validate_data(df10, "Query 10"):
            report['category_performance'] = df10
        
        return report
    
    def export_reports(self, output_dir='./data'):
        try:
            os.makedirs(output_dir, exist_ok=True)
            report = self.generate_report()
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            for name, df in report.items():
                if df is not None:
                    filename = f"{output_dir}/{name}_{timestamp}.csv"
                    df.to_csv(filename, index=False)
                    logging.info(f"📊 Report exported: {filename}")
            
            logging.info("✅ All reports exported successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Export failed: {e}")
            return False
    
    def close(self):
        if self.conn:
            self.conn.close()
            logging.info("✅ Database connection closed")

if __name__ == "__main__":
    try:
        db_name = os.getenv('DB_NAME', 'ecommerce_analytics')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = int(os.getenv('DB_PORT', 5432))
        
        if not db_password:
            logging.error("❌ DB_PASSWORD not set in .env file")
            exit(1)
        
        logging.info("🚀 Starting Analytics Pipeline")
        pipeline = AnalyticsPipeline(
            db_name=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        if not pipeline.connect():
            logging.error("❌ Failed to connect to database")
            exit(1)
        
        if pipeline.export_reports():
            logging.info("✅ Pipeline completed successfully!")
        else:
            logging.error("❌ Pipeline failed during export")
            exit(1)
        
    except Exception as e:
        logging.error(f"❌ Pipeline error: {e}")
        exit(1)
    
    finally:
        pipeline.close()
