from file_utils import get_data
from requests import post


def main():
	data = get_data()
	i = 0
	for k, v in data.items():
		resp = post("http://localhost:9200", data=v.encode('utf-8'))
		with open('proc/{}'.format(k), 'w', encoding='utf-8') as f:
			f.write(resp.text)
		print(i)
		i += 1


if __name__ == "__main__":
	main()
