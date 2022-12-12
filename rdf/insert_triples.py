from owlready2 import *
import json

onto = get_ontology("ontology.owl").load()

f = open('../scraping/results/22_23.json')
website = "https://www.zerozero.pt"
file = json.load(f)
print(file['FC Porto'][15])
league = onto.League("Liga_Portugal", leagueName=["Liga Portugal"], iden=["Liga_Portugal"])

edition = onto.Edition("22_23", editionYear=["22_23"], iden=["22_23"])
edition.editionOfLeague = league

idenCounter = 0
for x in file:
    clube = onto.Club(file[x][15].get("Nome")[0].replace(" ", "_"), clubFullName=file[x][15].get("Nome"),
                      clubSponsor=file[x][15].get("Patrocínio"), clubZeroZeroLink=[website + file[x][12]],
                      clubWebsite=file[x][15].get("Site Oficial"), clubAdress=file[x][15].get("Morada"),
                      clubPresident=file[x][15].get("Presidente"),
                      clubUefaRanking=[str(file[x][15].get("Rankings"))],
                      clubFoundationYear=file[x][15].get("Ano de Fundação"), clubCity=file[x][15].get("Cidade"),
                      clubEmail=file[x][15].get("E-mail"), clubImage=[file[x][-2]],
                      clubNickName=[file[x][15].get("Alcunhas")],
                      clubCountry=file[x][15].get("País"), clubMainSponsor=file[x][15].get("Marca Equipamento"),
                      iden=[file[x][15].get("Nome")[0].replace(" ", "_")],
                      clubAssociation=file[x][15].get("Associação"))

    squad = onto.Squad((file[x][15].get("Nome")[0] + "22_23").replace(" ", "_"), squadYear=[23],
                       iden=[(file[x][15].get("Nome")[0] + "22_23").replace(" ", "_")])
    squad.squadParticipatedIn = edition
    clube.clubHasSquad.append(squad)
    competitionsWon = file[x][16]
    for c in competitionsWon:
        item = competitionsWon[c]
        competition = onto.Competition(c.replace(" ", "_"), competitionName=[c], competitionNumber=[item],
                                       iden=[c.replace(" ", "_")])
        clube.clubWonCompetition.append(competition)

    player_info = file[x][13]
    for player in player_info:
        y = player_info[player]
        player = onto.Player(y[0].replace(" ", "_"), playerimage=[y[11]], playername=[y[0]], playernationality=[y[4]],
                             playernaturalFrom=[y[6]],
                             iden=[y[0].replace(" ", "_")],
                             playerposition=[y[7]], playerweight=[y[10]], playerheight=[y[9]], playerfoot=[y[8]],
                             playerbirthdate=[y[2]], playerage=[y[1]], playerbirthplace=[y[6]])
        player.playerPlayedForSquad.append(squad)
        player_records = y[12]
        for name in player_records:
            idenCounter += 1
            record = onto.Record("r_" + str(idenCounter), recordcompetitionname=[name],
                                 recordgames=[player_records[name][0]],
                                 recordminutes=[player_records[name][1]], recordgoals=[player_records[name][2]],
                                 iden=["r_" + str(idenCounter)],
                                 recordassists=[player_records[name][3]])
            player.playerHasRecord.append(record)
            record.recordForSquad = squad

        player_titles = y[13]
        for competition_name in player_titles:
            times = player_titles[competition_name]
            # print(competition_name)
            # print(player_item)
            player_competition = onto.Competition(competition_name.replace(" ", "_"),
                                                  competitionName=[competition_name],
                                                  iden=[competition_name.replace(" ", "_")])
            for i in range(int(times)):
                player.playerWonCompetition.append(player_competition)

editions = ["21_22", "20_21"]

for ed in editions:
    f = open("../scraping/results/" + ed + ".json")
    file = json.load(f)
    edition = onto.Edition(ed, editionYear=[ed], iden=[ed])
    edition.editionOfLeague = league

    for x in file:
        if onto[(file[x][15].get("Nome")[0]).replace(" ", "_")] == None:
            clube = onto.Club((file[x][15].get("Nome")[0]).replace(" ", "_"), clubFullName=file[x][15].get("Nome"),
                              clubSponsor=file[x][15].get("Patrocínio"), clubZeroZeroLink=[website + file[x][12]],
                              clubWebsite=file[x][15].get("Site Oficial"), clubAdress=file[x][15].get("Morada"),
                              clubPresident=file[x][15].get("Presidente"),
                              clubUefaRanking=[str(file[x][15].get("Rankings"))],
                              clubFoundationYear=file[x][15].get("Ano de Fundação"), clubCity=file[x][15].get("Cidade"),
                              clubEmail=file[x][15].get("E-mail"), clubImage=[file[x][-2]],
                              clubNickName=[file[x][15].get("Alcunhas")],
                              clubCountry=file[x][15].get("País"), clubMainSponsor=file[x][15].get("Marca Equipamento"),
                              iden=[(file[x][15].get("Nome")[0]).replace(" ", "_")],
                              clubAssociation=file[x][15].get("Associação"))

        else:
            clube = onto[(file[x][15].get("Nome")[0]).replace(" ", "_")]

        squad = onto.Squad((file[x][15].get("Nome")[0] + ed).replace(" ", "_"), squadYear=[23],
                           iden=[(file[x][15].get("Nome")[0] + ed).replace(" ", "_")])
        squad.squadParticipatedIn = edition
        clube.clubHasSquad.append(squad)

        player_info = file[x][13]
        for player in player_info:
            y = player_info[player]
            if onto[y[0].replace(" ", "_")] == None:
                player = onto.Player(y[0].replace(" ", "_"), playerimage=[y[11]], playername=[y[0]],
                                     playernationality=[y[4]], playernaturalFrom=[y[6]],
                                     playerposition=[y[7]], playerweight=[y[10]], playerheight=[y[9]],
                                     playerfoot=[y[8]], playerbirthdate=[y[2]], playerage=[y[1]],
                                     iden=[y[0].replace(" ", "_")],
                                     playerbirthplace=[y[6]])
            else:
                player = onto[y[0].replace(" ", "_")]

            player.playerPlayedForSquad.append(squad)
            player_records = y[12]
            for name in player_records:
                idenCounter += 1
                record = onto.Record("r_" + str(idenCounter), recordcompetitionname=[name],
                                     recordgames=[player_records[name][0]],
                                     recordminutes=[player_records[name][1]], recordgoals=[player_records[name][2]],
                                     iden=["r_" + str(idenCounter)],
                                     recordassists=[player_records[name][3]])
                record.recordForSquad = squad
                player.playerHasRecord.append(record)

for i in onto.Club.instances():
    print(i)

onto.save(file="result", format="rdfxml")
