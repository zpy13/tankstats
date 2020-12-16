from flask import Flask, render_template, request, redirect
import createdb as cdb
import sqlite3
import player as pl

app = Flask(__name__)

csv_reader = [cdb.read_csv() for _ in range(3)]

tiers = cdb.get_unique_values(csv_reader[0], 2)
countries = cdb.get_unique_values(csv_reader[1], 3)
types = cdb.get_unique_values(csv_reader[2], 4)

def make_query_with_db(query):
    ''' connect to the database and make the query, get the result
    
    Parameters
    ----------
    query
        text of query content
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect('tank_stats.sqlite')
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

def get_tank_by_tags(tier, country, type, ref = None):
    if ref:
        query = f"SELECT Tanks.* from Tanks,Tiers,Countries,Types where Tanks.TierId = Tiers.Id and Tiers.name = '{tier}' and Tanks.TypeId = Types.Id and Types.name = '{type}' ORDER BY Tanks.'{ref}' DESC"
    else:
        query = f"SELECT Tanks.* from Tanks,Tiers,Countries,Types where Tanks.TierId = Tiers.Id and Tiers.name = '{tier}' and Tanks.CountryId = Countries.Id and Countries.name = '{country}'and Tanks.TypeId = Types.Id and Types.name = '{type}'"
    tank_list = make_query_with_db(query)
    tank_output = []
    for tank in tank_list:
        tank = list(tank)
        tank[2] = tier
        tank[3] = country
        tank[4] = type
        for i in range(len(tank)):
            if tank[i] == '':
                tank[i] = 'N/A'
        tank_output.append(tank)
    new_tank_output = []
    for i in tank_output:
        if i in new_tank_output:
            None
        else:
            new_tank_output.append(i)
    return new_tank_output

def get_tank_by_name(name):
    query = f"SELECT Tanks.* from Tanks where Tanks.Name = '{name}'"
    tank = make_query_with_db(query)
    return tank

def get_column():
    connection = sqlite3.connect('tank_stats.sqlite')
    cursor = connection.execute('select * from Tanks')
    columns = [description[0] for description in cursor.description]
    connection.close()
    columns[2] = "Tier"
    columns[3] = "Country"
    columns[4] = "Type"
    return columns
    
def get_tags_from_name(name):
    query = f"SELECT Tiers.Name, Countries.Name, Types.Name FROM Tanks,Tiers,Countries,Types where Tanks.name = '{name}' and Tanks.CountryId = Countries.Id and Tanks.TypeId = Types.Id and Tanks.TierId = Tiers.Id"
    tags = make_query_with_db(query)
    return tags[0]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods = ['POST','GET'])
def search(): 
    return render_template('search.html',types = types, tiers = tiers, countries = countries)

@app.route('/search/results', methods = ['POST'])
def search_results():
    type = request.form['type']
    tier = request.form['tier']
    country = request.form['country']

    tank = get_tank_by_tags(tier, country, type)
    if not tank:
        return render_template('search_no_results.html')
    row_len = [i for i in range(len(tank))]
    column = get_column()
    col_len = [i for i in range(len(column))]
    return render_template('search_results.html',tank = tank, column = column, col_len = col_len, row_len = row_len)

@app.route('/compare',methods = ['POST','GET'])
def compare(): 
    ref = ["DPM", "Damage", "Penetration (mm)","Reload time (sec)","Aim time (sec)","Dispersion"]
    return render_template('compare.html',types = types, tiers = tiers, ref = ref)

@app.route('/comapre/results', methods = ['POST'])
def compare_results():
    type = request.form['type']
    tier = request.form['tier']
    ref = request.form['ref']
    tank = get_tank_by_tags(tier, " ", type, ref)
    if not tank:
        return render_template('compare_no_results.html')
    for i in range(len(tank)):
        country = get_tags_from_name(tank[i][1])[1]
        tank[i][3] = country
        
    row_len = [i for i in range(len(tank))]
    column = get_column()
    col_len = [i for i in range(len(column))]

    return render_template('compare_results.html', tank = tank, column = column, col_len = col_len, row_len = row_len)

@app.route('/tank')
def tank():
    return render_template('tank.html')

@app.route('/tank/results', methods = ['POST'])
def tank_results():
    name = request.form['name'] 
    return redirect(f'/tank/{name}')


@app.route('/tank/<name>')
def tank_name(name):
    
    tank = get_tank_by_name(name)
    if not tank:
        return render_template('tank_no_results.html')
    print(tank)
    tags = get_tags_from_name(name)
    tank = list(tank[0])
    tank[2] = tags[0]
    tank[3] = tags[1]
    tank[4] = tags[2]
    for i in range(len(tank)):
            if tank[i] == '':
                tank[i] = 'N/A'
    T = []
    T.append(tank)

    row_len = [i for i in range(len(T))]
    column = get_column()
    col_len = [i for i in range(len(column))]
    return render_template('tank_results.html',tank = T, column = column, col_len = col_len, row_len = row_len)

@app.route('/player')
def player_index():
    servers = ["EU","US","SEA","RU"]
    return render_template('player.html', servers = servers)

@app.route('/player/results', methods = ['POST'])
def player_results():
    server = request.form['server']
    player_id = request.form['player_id']
    return redirect(f'/player/{server}/{player_id}')

@app.route('/player/<server>/<player_id>')
def player_load(server,player_id):
    stats = pl.get_player_stats(server,player_id)
    if not stats:
        return render_template('player_no_results.html')
    title = f"Player: {player_id} from {server} server:"
    return render_template('player_results.html',title = title, stats = stats) 


@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)