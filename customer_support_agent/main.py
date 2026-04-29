from agent import CustomerSupportAgent

def main():
    agent = CustomerSupportAgent()
    print("客服系统已启动（输入 exit 退出）")

    while True:
        user_input = input("用户: ")
        if user_input.lower() == "exit":
            break
        response = agent.generate_response(user_input)
        print("客服:", response)

if __name__ == "__main__":
    main()
