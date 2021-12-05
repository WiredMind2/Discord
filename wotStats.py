import requests

nickname = input("Nickname: ")
rep = requests.get("https://worldoftanks.eu/en/community/accounts/#wot&at_search={}")
data = rep.content
data = data.split(b'<td class="b-user">')[1]
data = data.split(b'</td>')[0]
print(data)
