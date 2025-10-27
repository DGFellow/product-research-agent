"""
Search History Database
SQLite database for tracking research history
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from src.config import Config

class SearchHistoryDB:
    """Manage search history database"""
    
    def __init__(self):
        self.db_path = Config.DATA_DIR / "search_history.db"
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Searches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                platforms TEXT,  -- JSON: {"alibaba": true, "amazon": true}
                max_products INTEGER,
                total_results INTEGER,
                avg_margin REAL,
                best_margin REAL,
                status TEXT DEFAULT 'completed'
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER,
                source TEXT,
                title TEXT,
                price REAL,
                supplier_cost REAL,
                profit REAL,
                margin REAL,
                url TEXT,
                FOREIGN KEY (search_id) REFERENCES searches(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_search(self, search_term: str, platforms: Dict, max_products: int) -> int:
        """Add a new search record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO searches (search_term, platforms, max_products, status)
            VALUES (?, ?, ?, ?)
        ''', (search_term, json.dumps(platforms), max_products, 'in_progress'))
        
        search_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return search_id
    
    def update_search_results(self, search_id: int, total_results: int, 
                             avg_margin: float, best_margin: float):
        """Update search with final results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE searches
            SET total_results = ?, avg_margin = ?, best_margin = ?, status = 'completed'
            WHERE id = ?
        ''', (total_results, avg_margin, best_margin, search_id))
        
        conn.commit()
        conn.close()
    
    def add_product(self, search_id: int, source: str, title: str, price: float,
                   supplier_cost: float, profit: float, margin: float, url: str):
        """Add a product to a search"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (search_id, source, title, price, supplier_cost, profit, margin, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (search_id, source, title, price, supplier_cost, profit, margin, url))
        
        conn.commit()
        conn.close()
    
    def get_recent_searches(self, limit: int = 20) -> List[Dict]:
        """Get recent searches"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, search_term, timestamp, platforms, total_results, avg_margin, best_margin, status
            FROM searches
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        searches = []
        for row in rows:
            searches.append({
                'id': row[0],
                'search_term': row[1],
                'timestamp': row[2],
                'platforms': json.loads(row[3]) if row[3] else {},
                'total_results': row[4],
                'avg_margin': row[5],
                'best_margin': row[6],
                'status': row[7]
            })
        
        return searches
    
    def get_search_products(self, search_id: int) -> List[Dict]:
        """Get all products from a search"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT source, title, price, supplier_cost, profit, margin, url
            FROM products
            WHERE search_id = ?
        ''', (search_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            products.append({
                'source': row[0],
                'title': row[1],
                'price': row[2],
                'supplier_cost': row[3],
                'profit': row[4],
                'margin': row[5],
                'url': row[6]
            })
        
        return products
    
    def search_history(self, term: str) -> List[Dict]:
        """Search history by term"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, search_term, timestamp, platforms, total_results, avg_margin, best_margin
            FROM searches
            WHERE search_term LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{term}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        searches = []
        for row in rows:
            searches.append({
                'id': row[0],
                'search_term': row[1],
                'timestamp': row[2],
                'platforms': json.loads(row[3]) if row[3] else {},
                'total_results': row[4],
                'avg_margin': row[5],
                'best_margin': row[6]
            })
        
        return searches