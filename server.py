#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音电商数据看板 - 后端服务
"""

import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

PORT = 8088
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

class DashboardHandler(SimpleHTTPRequestHandler):
    """自定义HTTP处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/api/data':
            self.send_json(self.get_all_data())
        elif self.path.startswith('/api/data/'):
            data_type = self.path.split('/')[-1]
            self.send_json(self.get_data_by_type(data_type))
        else:
            super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self.save_data(data)
            self.send_json({'status': 'success', 'message': '数据已保存'})
        else:
            self.send_error(404)
    
    def send_json(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_all_data(self):
        """获取所有数据"""
        data_file = os.path.join(DATA_DIR, 'dashboard_data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_data()
    
    def get_data_by_type(self, data_type):
        """按类型获取数据"""
        all_data = self.get_all_data()
        return all_data.get(data_type, {})
    
    def save_data(self, data):
        """保存数据"""
        data_file = os.path.join(DATA_DIR, 'dashboard_data.json')
        
        # 读取现有数据
        existing_data = {}
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # 更新数据
        data_type = data.get('type', 'general')
        if data_type not in existing_data:
            existing_data[data_type] = []
        
        data['timestamp'] = datetime.now().isoformat()
        existing_data[data_type].append(data)
        
        # 保存数据
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    def get_default_data(self):
        """获取默认数据（618复盘数据）"""
        return {
            "overview": {
                "gmv": "2.5亿",
                "gmv_yoy": "+23.5%",
                "market_share": "25.57%",
                "market_share_yoy": "+0.35%",
                "vs_haier": "70.9%",
                "vs_haier_change": "-2.1%",
                "live_rooms": 66,
                "live_rooms_100w": 37
            },
            "sales": {
                "midea_share": 25.57,
                "haier_share": 35.9,
                "ronshen_share": 20.4,
                "vs_haier_ratio": 70.9,
                "avg_price": 2400,
                "problems": [
                    "美的十字入口跑输海尔",
                    "美的500行业资源未生效",
                    "两大主品牌份额均下滑"
                ],
                "solutions": [
                    "美的500充分参与平台资源",
                    "依托生态专供机型灵活承接补贴",
                    "完善产品价格矩阵"
                ]
            },
            "live": {
                "midea_rooms": 66,
                "haier_rooms": 98,
                "ronshen_rooms": 57,
                "ling_rooms": 55,
                "hualing_rooms": 29,
                "top50_midea": 16,
                "top50_haier": 19,
                "top50_ronshen": 15,
                "channel_compare": {
                    "官旗": 64,
                    "渠道号": 95,
                    "分销": 74,
                    "达人": 107
                }
            },
            "kol": {
                "midea_total": 16595.9,
                "haier_total": 19718.5,
                "midea_head": 2029.7,
                "haier_head": 3108.1,
                "vertical_ratio": 87.8,
                "natural_gap": 7200,
                "problems": [
                    "业绩高度集中垂类",
                    "头达差距明显",
                    "自然流场域阵地空白"
                ],
                "h2_targets": {
                    "head": 3000,
                    "vertical": 21000,
                    "natural": 6000
                }
            },
            "promotion": {
                "total_cost": 280,
                "cost_yoy": "+193%",
                "roi": 20.7,
                "roi_yoy": "-19%",
                "fee_rate": 10.5,
                "store_fee_rate": 4.6,
                "ice_flag": {
                    "cost": 117,
                    "roi": 35,
                    "yoy": "+23%"
                },
                "entrance": {
                    "cost": 106.5,
                    "roi": 15.9,
                    "yoy": "-39%"
                }
            },
            "video": {
                "views": 3947,
                "views_yoy": "+206%",
                "traffic": 121,
                "traffic_yoy": "+463%",
                "traffic_ratio": 30.3,
                "hot_count": 36,
                "million_count": 5,
                "top_video": {
                    "title": "美的508Pro冰箱 618必抢爆款",
                    "views": 438,
                    "traffic": 19.3
                }
            },
            "service": {
                "consult_volume": 156000,
                "consult_yoy": "+193%",
                "conversion_rate": 38,
                "conversion_yoy": "+19%",
                "avg_response": 28,
                "satisfaction": 81
            },
            "competitor": {
                "midea": {
                    "gmv": 2.5,
                    "share": 25.57,
                    "avg_price": 2400,
                    "live_rooms": 66
                },
                "haier": {
                    "gmv": 3.5,
                    "share": 35.9,
                    "avg_price": 2680,
                    "live_rooms": 98
                },
                "ronshen": {
                    "gmv": 2.0,
                    "share": 20.4,
                    "avg_price": 2150,
                    "live_rooms": 57
                }
            }
        }


def main():
    """启动服务器"""
    server = HTTPServer(('127.0.0.1', PORT), DashboardHandler)
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                    抖音电商数据看板                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   服务已启动: http://127.0.0.1:{PORT}                           ║
║                                                               ║
║   API接口:                                                    ║
║     - GET  /api/data          获取所有数据                     ║
║     - GET  /api/data/{type}   获取指定类型数据                  ║
║     - POST /api/data          保存数据                        ║
║                                                               ║
║   按 Ctrl+C 停止服务                                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.shutdown()


if __name__ == '__main__':
    main()
