cities = ["Ahmadabad","Naroda","Naroda","Narora","Narora","Sabarmati Junction","Sabarmati Junction","Sabarmati","Sabarmati","Watuwa","Watuwa","Batwa","Batwa","Vejalpur","Vejalpur","Wanch","Wanch","Sarkhej","Sarkhej","Vehelal","Vehelal","Vahelala","Vahelala","Adalaj","Adalaj","Jetalpur","Jetalpur","Satej","Satej","Uwarsad","Uwarsad","Dabhoda","Dabhoda","Kanij","Kanij","Kasandra","Kasandra","Sanand","Sanand","Dahegam","Dahegam","Dehgam","Dehgam","Badarpur","Badarpur","Ghorasar","Ghorasar"]
cities = sorted(list(set(cities)))
crimes = ["Barratry",
"Battery",
"Blackmail",
"Blasphemous libel",
"Blockbusting",
"Body snatching",
"Bomb threat",
"Breach of the peace"]

def mkChoice(data):
    choice=[]
    for d in data:
        d = d.lower()
        choice.append(
            (c.replace(' ', '_'), c)
        )
    return tuple(choice)