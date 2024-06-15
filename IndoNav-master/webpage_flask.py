from flask import Flask, render_template, request, jsonify
import json
import heapq

app = Flask(__name__)

# Load edges data from JSON file or define it directly in the code
edges_dict = {
              'room101': {'101nav152': 1.5},
              'room152': {'101nav152': 1.5},
              'room102': {'102nav151': 1.5},
              'room151': {'102nav151': 1.5},
              'room103': {'103nav': 1.5},
              'room104': {'104nav150': 1.5},
              'room150': {'104nav150': 1.5},
              'room105': {'105nav': 1.5},
              'room149': {'149nav': 1.5},
              'room106': {'106nav': 1.5},
              'room148': {'148nav': 1.5},
              'room107': {'107nav': 1.5},
              'room108': {'108nav': 1.5},
              'room109': {'109nav': 1.5},
              'room110': {'110nav': 1.5},
              'room111': {'111nav147': 1.5},
              'room147': {'111nav147': 1.5},
              'room112': {'112nav146': 1.5},
              'room146': {'112nav146': 1.5},
              'room113': {'113nav145': 1.5},
              'room145': {'113nav145': 1.5},
              'room114': {'114nav133': 1.5},
              'room133': {'114nav133': 1.5},
              'room115': {'115nav132': 1.5},
              'room132': {'115nav132': 1.5},
              'room116': {'116nav131': 1.5},
              'room131': {'116nav131': 1.5},
              'room117': {'117nav': 1.5},
              'room118': {'118nav': 1.5},
              'room119': {'119nav': 1.5},
              'room120': {'120nav': 1.5},
              'room121': {'121nav130': 1.5},
              'room130': {'121nav130': 1.5},
              'room122': {'122nav': 1.5},
              'room123': {'123nav129': 1.5},
              'room129': {'123nav129': 1.5},
              'room124': {'124nav': 1.5},
              'room125': {'125nav128': 1.5},
              'room128': {'125nav128': 1.5},
              'room126': {'126nav127': 1.5},
              'room127': {'126nav127': 1.5},
              'room144': {'144nav': 1},
              'room143': {'143nav': 1},
              'room142': {'142nav': 1.5},
              'room141': {'141nav': 1.5},
              'room140': {'navcs1': 1.5},
              'room139': {'139nav': 1.5},
              'room138': {'138nav': 1.5},
              'room137': {'137nav': 1},
              'room136': {'136nav': 1},
              'room135': {'135nav': 1, 'room134': 4},
              'room134': {'room135': 4},

              '101nav152': {'room101': 1.5, 'room152': 1.5, '102nav151': 4},
              '102nav151': {'101nav152': 4, 'room102': 1.5, 'room151': 1.5, '103nav': 7},
              '103nav': {'102nav151': 7, '104nav150': 7, 'east_stair1': 9},
              '104nav150': {'103nav': 7, 'room104': 1.5, 'room150': 1.5, '105nav': 2},
              '105nav': {'104nav250': 2, 'room105': 1.5, '149nav': 3},
              '149nav': {'room149': 1.5, '105nav': 3, '106nav': 2},
              '106nav': {'room106': 1.5, '149nav': 2, '148nav': 2},
              '148nav': {'room148': 1.5, '106nav': 2, '107nav': 5},
              '107nav': {'room107': 1.5, '148nav': 5, '108nav': 3},
              '108nav': {'room108': 1.5, '107nav': 3, '109nav': 7},
              '109nav': {'room109': 1.5, '108nav': 7, '110nav': 7},
              '110nav': {'room110': 1.5, '111nav147': 7, '109nav': 7, '210nav': 13},
              '111nav147': {'110nav': 7, 'room111': 1.5, 'room147': 1.5, '112nav146': 7},
              '112nav146': {'111nav147': 7, '113nav145': 7, 'room112': 1.5, 'room146': 1.5},
              '113nav145': {'112nav146': 7, 'room112': 1.5, 'room146': 1.5, 'lounge1': 5},
              'lounge1': {'loungelane1': 22, '113nav145': 5, '114nav133': 10},
              '114nav133': {'lounge1': 10, '115nav132': 7, 'room114': 1.5, 'room133': 1.5},
              '115nav132': {'114nav133': 7, '116nav131': 7, 'room115': 1.5, 'room132': 1.5},
              '116nav131': {'115nav132': 7, '117nav': 1.5, 'room116': 1.5, 'room131': 1.5},
              '117nav': {'room117': 1.5, '116nav131': 1.5, '118nav': 6, '217nav': 13},
              '118nav': {'room118': 1.5, '117nav': 6, '119nav': 7},
              '119nav': {'room119': 1.5, '118nav': 7, '120nav': 3},
              '120nav': {'room120': 1.5, '119nav': 3, '121nav130': 9},
              '121nav130': {'120nav': 9, '122nav': 7, 'room121': 1.5, 'room130': 1.5},
              '122nav': {'room122': 1.5, '121nav130': 7, '123nav129': 8},
              '123nav129': {'122nav': 8, '124nav': 3, 'room123': 1.5, 'room129': 1.5},
              '124nav': {'123nav129': 3, '125nav128': 7, 'room124': 1.5, 'navce1': 22},
              '125nav128': {'124nav': 7, '126nav127': 4, 'room125': 1.5, 'room128': 1.5},
              '126nav127': {'125nav128': 4, 'room126': 1.5, 'room127': 1.5},
              'loungelane1': {'lounge1': 22, '144nav': 6, '134nav': 6},
              '144nav': {'loungelane1': 6, 'room144': 1, '143nav': 8},
              '143nav': {'144nav': 8, 'room143': 1, '142nav': 8},
              '142nav': {'room142': 1, 'navcw1': 2, 'navcn1': 5, '143nav': 8},
              'navcw1': {'east_stair': 10, 'navcs1': 5, '141nav': 3, '142nav': 2},
              '141nav': {'room141': 1, 'navcw1': 3, 'navcs1': 3},
              'navcs1': {'141nav': 3, 'navcw1': 5, 'room140': 2, '139nav': 3, 'navce1': 5},
              '139nav': {'room139': 2, 'navcs1': 3, 'navce1': 3},
              'navce1': {'124nav': 22, 'navcs1': 5, 'navcn1': 5, '139nav': 3, '138nav': 2},
              'navcn1': {'navcw1': 5, 'navce1': 5, '142nav': 4, '138nav': 5, '137nav': 4},
              '138nav': {'navce1': 2, 'navcn1': 5, '137nav': 4, 'room138': 1},
              '137nav': {'navcn1': 4, '138nav': 4, '136nav': 4, 'room137': 1},
              '136nav': {'137nav': 4, '135nav': 4, 'room136': 1},
              '135nav': {'136nav': 4, 'room135': 1, 'room134': 4},
              '134nav': {'loungelane1': 6, '135nav': 4},
              'east_stair1': {'103nav': 9, 'east_stair2': 13, 'navcw1': 10},

              'room201': {'201nav252': 1.5},
              'room252': {'201nav252': 1.5},
              'room202': {'202nav251': 1.5},
              'room251': {'202nav251': 1.5},
              'room203': {'203nav': 1.5},
              'room204': {'204nav250': 1.5},
              'room250': {'204nav250': 1.5},
              'room205': {'205nav': 1.5},
              'room249': {'249nav': 1.5},
              'room206': {'206nav': 1.5},
              'room248': {'248nav': 1.5},
              'room207': {'207nav': 1.5},
              'room208': {'208nav': 1.5},
              'room209': {'209nav': 1.5},
              'room210': {'210nav': 1.5},
              'room211': {'211nav247': 1.5},
              'room247': {'211nav247': 1.5},
              'room212': {'212nav246': 1.5},
              'room246': {'212nav246': 1.5},
              'room213': {'213nav245': 1.5},
              'room245': {'213nav245': 1.5},
              'room214': {'214nav233': 1.5},
              'room233': {'214nav233': 1.5},
              'room215': {'215nav232': 1.5},
              'room232': {'215nav232': 1.5},
              'room216': {'216nav231': 1.5},
              'room231': {'216nav231': 1.5},
              'room217': {'217nav': 1.5},
              'room218': {'218nav': 1.5},
              'room219': {'219nav': 1.5},
              'room220': {'220nav': 1.5},
              'room221': {'221nav230': 1.5},
              'room230': {'221nav230': 1.5},
              'room222': {'222nav': 1.5},
              'room223': {'223nav229': 1.5},
              'room229': {'223nav229': 1.5},
              'room224': {'224nav': 1.5},
              'room225': {'225nav228': 1.5},
              'room228': {'225nav228': 1.5},
              'room226': {'226nav227': 1.5},
              'room227': {'226nav227': 1.5},
              'room244': {'244nav': 1},
              'room243': {'243nav': 1},
              'room242': {'242nav': 1.5},
              'room241': {'241nav': 1.5},
              'room240': {'navcs2': 1.5},
              'room239': {'239nav': 1.5},
              'room238': {'238nav': 1.5},
              'room237': {'237nav': 1},
              'room236': {'236nav': 1},
              'room235': {'235nav': 1, 'room234': 4},
              'room234': {'room235': 4},

              '201nav252': {'202nav251': 4, 'room201': 1.5, 'room252': 1.5},
              '202nav251': {'201nav252': 4, 'room202': 1.5, 'room251': 1.5, '203nav': 7},
              '203nav': {'202nav251': 7, '204nav250': 7, 'east_stair2': 9},
              '204nav250': {'203nav': 7, 'room204': 1.5, 'room250': 1.5, '205nav': 2},
              '205nav': {'204nav250': 2, 'room205': 1.5, '249nav': 3},
              '249nav': {'room249': 1.5, '205nav': 3, '206nav': 2},
              '206nav': {'room206': 1.5, '249nav': 2, '248nav': 2},
              '248nav': {'room248': 1.5, '206nav': 2, '207nav': 5},
              '207nav': {'room207': 1.5, '248nav': 5, '208nav': 3},
              '208nav': {'room208': 1.5, '207nav': 3, '209nav': 7},
              '209nav': {'room209': 1.5, '208nav': 7, '210nav': 7},
              '210nav': {'room210': 1.5, '211nav247': 7, '209nav': 7, '110nav': 13, '310nav': 13},
              '211nav247': {'210nav': 7, 'room211': 1.5, 'room247': 1.5, '212nav246': 7},
              '212nav246': {'211nav247': 7, '213nav245': 7, 'room212': 1.5, 'room246': 1.5},
              '213nav245': {'212nav246': 7, 'room212': 1.5, 'room246': 1.5, 'lounge2': 5},
              'lounge2': {'loungelane2': 22, '213nav245': 5, '214nav233': 10},
              '214nav233': {'lounge2': 10, '215nav232': 7, 'room214': 1.5, 'room233': 1.5},
              '215nav232': {'214nav233': 7, '216nav231': 7, 'room215': 1.5, 'room232': 1.5},
              '216nav231': {'215nav232': 7, '217nav': 1.5, 'room216': 1.5, 'room231': 1.5},
              '217nav': {'room217': 1.5, '216nav231': 1.5, '218nav': 6, '117nav': 13, '317nav': 13},
              '218nav': {'room218': 1.5, '217nav': 6, '219nav': 7},
              '219nav': {'room219': 1.5, '218nav': 7, '220nav': 3},
              '220nav': {'room220': 1.5, '219nav': 3, '221nav230': 9},
              '221nav230': {'220nav': 9, '222nav': 7, 'room221': 1.5, 'room230': 1.5},
              '222nav': {'room222': 1.5, '221nav230': 7, '223nav229': 8},
              '223nav229': {'222nav': 8, '224nav': 3, 'room223': 1.5, 'room229': 1.5},
              '224nav': {'223nav229': 3, '225nav228': 7, 'room224': 1.5, 'navce2': 22},
              '225nav228': {'224nav': 7, '226nav227': 4, 'room225': 1.5, 'room228': 1.5},
              '226nav227': {'225nav228': 4, 'room226': 1.5, 'room227': 1.5},
              'loungelane2': {'lounge2': 22, '244nav': 6, '234nav': 6},
              '244nav': {'loungelane2': 6, 'room244': 1, '243nav': 8},
              '243nav': {'244nav': 8, 'room243': 1, '242nav': 8},
              '242nav': {'room242': 1, 'navcw2': 2, 'navcn2': 5, '243nav': 8},
              'navcw2': {'east_stair2': 10, 'navcs2': 5, '241nav': 3, '242nav': 2},
              '241nav': {'room241': 1, 'navcw2': 3, 'navcs2': 3},
              'navcs2': {'241nav': 3, 'navcw2': 5, 'room240': 2, '239nav': 3, 'navce2': 5},
              '239nav': {'room239': 2, 'navcs2': 3, 'navce2': 3},
              'navce2': {'224nav': 22, 'navcs2': 5, 'navcn2': 5, '239nav': 3, '238nav': 2},
              'navcn2': {'navcw2': 5, 'navce2': 5, '242nav': 4, '238nav': 5, '237nav': 4},
              '238nav': {'navce2': 2, 'navcn2': 5, '237nav': 4, 'room238': 1},
              '237nav': {'navcn2': 4, '238nav': 4, '236nav': 4, 'room237': 1},
              '236nav': {'237nav': 4, '235nav': 4, 'room236': 1},
              '235nav': {'236nav': 4, 'room235': 1, 'room234': 4},
              '234nav': {'loungelane2': 6, '235nav': 4},
              'east_stair2': {'203nav': 9, 'navcw2': 10, 'east_stair3': 13, 'east_stair1': 13},

              'roo301': {'301nav352': 1.5},
              'room352': {'301nav352': 1.5},
              'room302': {'302nav351': 1.5},
              'room351': {'302nav351': 1.5},
              'room303': {'303nav': 1.5},
              'room304': {'304nav350': 1.5},
              'room350': {'304nav350': 1.5},
              'room305': {'305nav': 1.5},
              'room349': {'349nav': 1.5},
              'room306': {'306nav': 1.5},
              'room348': {'348nav': 1.5},
              'room307': {'307nav': 1.5},
              'room308': {'308nav': 1.5},
              'room309': {'309nav': 1.5},
              'room310': {'310nav': 1.5},
              'room311': {'311nav347': 1.5},
              'room347': {'311nav347': 1.5},
              'room312': {'312nav346': 1.5},
              'room346': {'312nav346': 1.5},
              'room313': {'313nav345': 1.5},
              'room345': {'313nav345': 1.5},
              'room314': {'314nav333': 1.5},
              'room333': {'314nav333': 1.5},
              'room315': {'315nav332': 1.5},
              'room332': {'315nav332': 1.5},
              'room316': {'316nav331': 1.5},
              'room331': {'316nav331': 1.5},
              'room317': {'317nav': 1.5},
              'room318': {'318nav': 1.5},
              'room319': {'319nav': 1.5},
              'room320': {'320nav': 1.5},
              'room321': {'321nav330': 1.5},
              'room330': {'321nav330': 1.5},
              'room322': {'322nav': 1.5},
              'room323': {'323nav329': 1.5},
              'room329': {'323nav329': 1.5},
              'room324': {'324nav': 1.5},
              'room325': {'325nav328': 1.5},
              'room328': {'325nav328': 1.5},
              'room326': {'326nav327': 1.5},
              'room327': {'326nav327': 1.5},
              'room344': {'344nav': 1},
              'room343': {'343nav': 1},
              'room342': {'342nav': 1.5},
              'room341': {'341nav': 1.5},
              'room340': {'navcs3': 1.5},
              'room339': {'339nav': 1.5},
              'room338': {'338nav': 1.5},
              'room337': {'337nav': 1},
              'room336': {'336nav': 1},
              'room335': {'335nav': 1, 'room334': 4},
              'room334': {'room335': 4},
              '301nav352': {'302nav351': 4, 'room301': 1.5, 'room352': 1.5},
              '302nav351': {'301nav352': 4, 'room302': 1.5, 'room351': 1.5, '303nav': 7},
              '303nav': {'302nav351': 7, '304nav350': 7, 'east_stair3': 9},
              '304nav350': {'303nav': 7, 'room304': 1.5, 'room350': 1.5, '305nav': 2},
              '305nav': {'304nav350': 2, 'room305': 1.5, '349nav': 3},
              '349nav': {'room349': 1.5, '305nav': 3, '306nav': 2},
              '306nav': {'room306': 1.5, '349nav': 2, '348nav': 2},
              '348nav': {'room348': 1.5, '306nav': 2, '307nav': 5},
              '307nav': {'room307': 1.5, '348nav': 5, '308nav': 3},
              '308nav': {'room308': 1.5, '307nav': 3, '309nav': 7},
              '309nav': {'room309': 1.5, '308nav': 7, '310nav': 7},
              '310nav': {'room310': 1.5, '311nav347': 7, '309nav': 7, '210nav': 13},
              '311nav347': {'310nav': 7, 'room311': 1.5, 'room347': 1.5, '312nav346': 7},
              '312nav346': {'311nav347': 7, '313nav345': 7, 'room312': 1.5, 'room346': 1.5},
              '313nav345': {'312nav346': 7, 'room312': 1.5, 'room346': 1.5, 'lounge3': 5},
              'lounge3': {'loungelane3': 22, '313nav345': 5, '314nav333': 10},
              '314nav333': {'lounge3': 10, '315nav332': 7, 'room314': 1.5, 'room333': 1.5},
              '315nav332': {'314nav333': 7, '316nav331': 7, 'room315': 1.5, 'room332': 1.5},
              '316nav331': {'315nav332': 7, '317nav': 1.5, 'room316': 1.5, 'room331': 1.5},
              '317nav': {'room317': 1.5, '316nav331': 1.5, '318nav': 6, '217nav': 13},
              '318nav': {'room318': 1.5, '317nav': 6, '319nav': 7},
              '319nav': {'room319': 1.5, '318nav': 7, '320nav': 3},
              '320nav': {'room320': 1.5, '319nav': 3, '321nav330': 9},
              '321nav330': {'320nav': 9, '322nav': 7, 'room321': 1.5, 'room330': 1.5},
              '322nav': {'room322': 1.5, '321nav330': 7, '323nav329': 8},
              '323nav329': {'322nav': 8, '324nav': 3, 'room323': 1.5, 'room329': 1.5},
              '324nav': {'323nav329': 3, '325nav328': 7, 'room324': 1.5, 'navce3': 22},
              '325nav328': {'324nav': 7, '326nav327': 4, 'room325': 1.5, 'room328': 1.5},
              '326nav327': {'325nav328': 4, 'room326': 1.5, 'room327': 1.5},
              'loungelane3': {'lounge3': 22, '344nav': 6, '334nav': 6},
              '344nav': {'loungelane3': 6, 'room344': 1, '343nav': 8},
              '343nav': {'344nav': 8, 'room343': 1, '342nav': 8},
              '342nav': {'room342': 1, 'navcw3': 2, 'navcn3': 5, '343nav': 8},
              'navcw3': {'east_stair3': 10, 'navcs3': 5, '341nav': 3, '342nav': 2},
              '341nav': {'room341': 1, 'navcw3': 3, 'navcs3': 3},
              'navcs3': {'341nav': 3, 'navcw3': 5, 'room340': 2, '339nav': 3, 'navce3': 5},
              '339nav': {'room339': 2, 'navcs3': 3, 'navce3': 3},
              'navce3': {'324nav': 22, 'navcs3': 5, 'navcn3': 5, '339nav': 3, '338nav': 2},
              'navcn3': {'navcw3': 5, 'navce3': 5, '342nav': 4, '338nav': 5, '337nav': 4},
              '338nav': {'navce3': 2, 'navcn3': 5, '337nav': 4, 'room338': 1},
              '337nav': {'navcn3': 4, '338nav': 4, '336nav': 4, 'room337': 1},
              '336nav': {'337nav': 4, '335nav': 4, 'room336': 1},
              '335nav': {'336nav': 4, 'room335': 1, 'room334': 4},
              '334nav': {'loungelane3': 6, '335nav': 4},
              'east_stair3': {'303nav': 9, 'navcw3': 10, 'east_stair2': 13}

              }


# Dijkstra's algorithm implementation
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            if node == end:
                return cost, path

            for neighbor, weight in graph.get(node, {}).items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
    return float("inf"), []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_path", methods=["POST"])
def get_path():
    data = request.get_json()
    source = data['source']
    destination = data['destination']

    distance, path = dijkstra(edges_dict, source, destination)

    if path:
        return jsonify({"path": path, "distance": distance}), 200
    else:
        return jsonify({"error": "No path found for the given source and destination."}), 404


if __name__ == "__main__":
    app.run(debug=True)
