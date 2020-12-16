import csv
import sqlite3

def create_db():
    ''' create database with sql
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    '''
    conn = sqlite3.connect('tank_stats.sqlite')
    cur = conn.cursor()

    drop_tanks_sql = 'DROP TABLE IF EXISTS "Tanks"'
    drop_tiers_sql = 'DROP TABLE IF EXISTS "Tiers"'
    drop_countries_sql = 'DROP TABLE IF EXISTS "Countries"'
    drop_types_sql = 'DROP TABLE IF EXISTS "Types"'

    create_tanks_sql = '''
        CREATE TABLE IF NOT EXISTS "Tanks" (
            "Id"	INTEGER PRIMARY KEY,
            "Name"	TEXT,
            "TierId"	INTEGER NOT NULL,
            "CountryId"	INTEGER NOT NULL,
            "TypeId"	INTEGER NOT NULL,
            "DPM"	TEXT,
            "Damage"	TEXT,
            "Penetration (mm)"	INTEGER,
            "Reload time (sec)"	TEXT,
            "Rate of fire (rnds/min)"	REAL,
            "Aim time (sec)"	REAL,
            "Dispersion"	REAL,
            "Gun handling when moving"	REAL,
            "Gun handling when tank traverse"	REAL,
            "Gun handling when turret traverse"	REAL,
            "Gun handling when after firing"	REAL,
            "Gun handling when damaged"	REAL,
            "Damage vs. modules"	INTEGER,
            "Caliber (mm)"	REAL,
            "Shell velocity (m/s)"	TEXT,
            "Max range (m)"	TEXT,
            "Ammo capacity"	INTEGER,
            "Potential damage"	TEXT,
            "Shell cost"	TEXT,
            "Top speed (km/h)"	REAL,
            "Reverse speed (km/h)"	REAL,
            "Power (hp)"	TEXT,
            "Power/weight (hp/t)"	REAL,
            "Tank traverse (°/sec)"	REAL,
            "Effective traverse hard (°/sec)"	REAL,
            "Effective traverse medium (°/sec)"	REAL,
            "Effective traverse soft (°/sec)"	REAL,
            "Terrain resistance hard"	REAL,
            "Terrain resistance medium"	REAL,
            "Terrain resistance soft"	REAL,
            "Gun elevation (°)"	REAL,
            "Gun depression (°)"	REAL,
            "Gun traverse (°/sec)"	REAL,
            "Gun traverse range (°)"	TEXT,
            "Turret traverse (°/sec)"	REAL,
            "Hull armor (mm)"	TEXT,
            "Turret armor (mm)"	TEXT,
            "Track armor (mm)"	INTEGER,
            "Health"	TEXT,
            "Engine health"	INTEGER,
            "Track health"	INTEGER,
            "Track health repaired"	INTEGER,
            "Ammo rack health"	INTEGER,
            "Fuel tank health"	INTEGER,
            "Max load (kg)"	TEXT,
            "Total weight (kg)"	TEXT,
            "Stationary camo (%)"	TEXT,
            "Moving camo (%)"	TEXT,
            "View range (m)"	INTEGER,
            "Radio range (m)"	REAL,
            "Fire chance"	TEXT,
            "Tank cost"	TEXT,
            "Clip size"	REAL,
            "Clip damage"	TEXT,
            "Intra-clip reload"	REAL,
            "Explosion radius"	REAL,
            "Max Wheel Angle (°)"	REAL,
            "Axle Count"	REAL,
            "Alt. gun (sec)"	REAL,
            "Charge/lock (sec)"	TEXT,
            FOREIGN KEY("CountryId") REFERENCES "Countries"("Id"),
	        FOREIGN KEY("TypeId") REFERENCES "Types"("Id"),
	        FOREIGN KEY("TierId") REFERENCES "Tiers"("Id")
        )
    '''
    create_tiers_sql = '''
        CREATE TABLE IF NOT EXISTS 'Tiers'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL
        )
    '''
    create_countries_sql = '''
        CREATE TABLE IF NOT EXISTS 'Countries'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL
        )
    '''
    create_types_sql = '''
        CREATE TABLE IF NOT EXISTS 'Types'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL
        )
    '''

    cur.execute(drop_tanks_sql)
    cur.execute(drop_tiers_sql)
    cur.execute(drop_countries_sql)
    cur.execute(drop_types_sql)

    
    cur.execute(create_tiers_sql)
    cur.execute(create_countries_sql)
    cur.execute(create_types_sql)
    cur.execute(create_tanks_sql)

    conn.commit()
    conn.close()

def read_csv():
    ''' read csv files and output csv_reader list
    
    Parameters
    ----------
    None

    Returns
    -------
    list
        csv_reader
    '''
    file_contents = open('tankstats_stats_modified.csv', 'r', encoding='UTF-8')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)
    return csv_reader

def get_unique_values(csv_reader, num):
    ''' remove the repeated values and get the unique values in a field
    
    Parameters
    ----------
    list
        csv_reader
    num
        field number

    Returns
    -------
    list
        unique values
    '''
    values = []
    for row in csv_reader:
        if row[num] not in values:
            values.append(row[num])
    return values

def load_tiers():
    ''' load tiers table from csv

    '''
    conn = sqlite3.connect('tank_stats.sqlite')
    cur = conn.cursor()

    csv_reader = read_csv()
    tiers = get_unique_values(csv_reader, 2)

    insert_tier_sql = '''
        INSERT INTO Tiers
        VALUES (NULL, ?)
    '''
    for tier in tiers:
        cur.execute(insert_tier_sql,[tier])
    conn.commit()
    conn.close()

def load_countries():
    ''' load countries table from csv
    
    '''

    conn = sqlite3.connect('tank_stats.sqlite')
    cur = conn.cursor()

    csv_reader = read_csv()
    countries = get_unique_values(csv_reader, 3)

    insert_country_sql = '''
        INSERT INTO Countries
        VALUES (NULL, ?)
    '''
    for country in countries:
        cur.execute(insert_country_sql,[country])
    conn.commit()
    conn.close()

def load_types():
    ''' load types table from csv
    
    '''
    conn = sqlite3.connect('tank_stats.sqlite')
    cur = conn.cursor()

    csv_reader = read_csv()
    types = get_unique_values(csv_reader, 4)

    insert_type_sql = '''
        INSERT INTO Types
        VALUES (NULL, ?)
    '''
    for type in types:
        cur.execute(insert_type_sql,[type])
    conn.commit()
    conn.close()

def load_tanks():
    ''' load tanks table from csv
    
    '''
    conn = sqlite3.connect('tank_stats.sqlite')
    cur = conn.cursor()

    csv_reader = read_csv()

    select_tier_id_sql = '''
        SELECT Id FROM Tiers
        WHERE Name = ?
    '''
    select_country_id_sql = '''
        SELECT Id FROM Countries
        WHERE Name = ?
    '''
    select_type_id_sql = '''
        SELECT Id FROM Types
        WHERE Name = ?
    '''

    insert_tank_sql = '''
        INSERT INTO Tanks
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    for row in csv_reader:

        cur.execute(select_tier_id_sql,[row[2]])
        res = cur.fetchone()
        tier_id = None
        if res is not None:
            tier_id = res[0]

        cur.execute(select_country_id_sql,[row[3]])
        res = cur.fetchone()
        country_id = None
        if res is not None:
            country_id = res[0]
    
        cur.execute(select_type_id_sql,[row[4]])
        res = cur.fetchone()
        type_id = None
        if res is not None:
            type_id = res[0]

        row_list = []
        for item in row:
            row_list.append(item)
        row_list[2] = tier_id
        row_list[3] = country_id
        row_list[4] = type_id

        cur.execute(insert_tank_sql, row_list)
    conn.commit()
    conn.close()    

create_db()
load_tiers()
load_countries()
load_types()
load_tanks()