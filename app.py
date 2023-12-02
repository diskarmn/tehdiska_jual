import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template,request,url_for,jsonify,redirect
from pymongo import MongoClient
app=Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db=client[DB_NAME]


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/pemberitahuan',methods=['GET'])
def pemberitahuan():
    return render_template('pemberitahuan.html')

@app.route("/tampil",methods=['GET'])
def tampil():
    semua=list(db.pelanggan.find({},{'_id': False}))
    return jsonify({'semua':semua})

@app.route("/tampilp",methods=['GET'])
def tampilp():
    semuap=list(db.status.find({},{'_id': False}))
    return jsonify({'semuap':semuap})

@app.route('/selesai',methods=['POST'])
def selesai():
    selesai=request.form['nomor']
    db.pelanggan.update_one(
        {'num':int(selesai)},
        {'$set':{'status':'selesai'}}
    )    
    return jsonify({'pesan':'berhasil mengubah info pesanan'})

@app.route('/hapus',methods=['POST'])
def hapus():
    hapus=request.form['hapus']
    db.pelanggan.delete_one(
        {'num':int(hapus)})    
    return jsonify({'pesan':'berhasil menghapus pesanan'})

@app.route('/ubah',methods=['POST'])
def ubah():
    nomor=request.form['knomor']
    pesan=request.form['kpesan']
    original=request.form['koriginal']
    strawberry=request.form['kstrawberry']
    db.status.update_one(
        {'nomor':int(nomor)},
        {'$set':{'pesan': pesan,
        'original': original,
        'strawberry': strawberry}}
    )    
    return jsonify({'pesan':'berhasil mengubah info pesanan'})



if __name__=='__main__':
    app.run('0.0.0.0',port=5001,debug=True)