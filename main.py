import argparse

if __name__ == '__main__':
    # 从命令行获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
       '-u', '--url',
        dest='url', type=str, help='Server url.Could be ip address or hostname', required=True)
    parser.add_argument(
       '-t' ,'--token',
        dest='token', type=str, help='Optional Server token.', required=False)
    args = parser.parse_args()