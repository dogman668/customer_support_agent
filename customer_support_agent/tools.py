def get_order_status(order_id):
    fake_db = {"123": "已发货", "456": "运输中", "789": "已完成"}
    return fake_db.get(order_id, "未找到订单")

def create_ticket(user_input):
    return f"已为您创建工单，我们会尽快联系您。问题：{user_input}"
