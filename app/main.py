from flask import Flask, jsonify, request
from urllib import response
from flask_restful import Resource, Api
from flask_cors import CORS
import pandas as pd
import numpy as np
from random import choice

df = pd.read_csv('DATA_CORR.csv', index_col=['Unnamed: 0'])
df2 = pd.read_csv('Kode_produk.csv')


# class Test(Resource):
@app.route('/products', methods=['POST'])
def post():
    try:
        x = request.json['product']
        text = 'Produk_' + x
        # {START "INI KALAU ADA KORELASI REKOMENDASI"}
        if len(df[df.columns == text]) != 0:
            product_recomend = df[df[text] > 0][text].index
            recomend_lain = df2['produk'].values

            recomend_sementara = []
            for n in product_recomend:
                # {START "JIKA REKOMENDASI DIBERIKAN ADALAH DENGAN DIRINYA SENDIRI MAKA DI SKIP"}
                if n != text:
                    n = n.split('_')[1]
                    recomend_sementara.append(n)
                # {END "JIKA REKOMENDASI DIBERIKAN ADALAH DENGAN DIRINYA SENDIRI MAKA DI SKIP"}

            n_recomend = 10
            condition = n_recomend - len(recomend_sementara)

            # {START "KALAU TERNYATA REKOMENDASI_SEMENTARA < 10 MAKA DITAMBAKAN DENGAN PRODUK ACAK"}
            if condition > 0:
                list_rekomendasi_lain = []
                for i in range(condition):
                    n_rekomendasi_lain = choice(recomend_lain)
                    list_rekomendasi_lain.append(n_rekomendasi_lain)
                recomend = np.concatenate(
                    (recomend_sementara, list_rekomendasi_lain))

            # {END "KALAU TERNYATA REKOMENDASI_SEMENTARA < 10 MAKA DITAMBAKAN DENGAN PRODUK ACAK"}

            # {START "KALAU TERNYATA REKOMENDASI_SEMENTARA > 10 MAKA REKOMENDASI_SEMENTARA ADALAH SOLUASI"}
            else:
                recomend = recomend_sementara

                # result = {'result': recomend}
                # return result
            # {END "KALAU TERNYATA REKOMENDASI_SEMENTARA > 10 MAKA REKOMENDASI_SEMENTARA ADALAH SOLUASI"}
        # {END "INI KALAU ADA KORELASI REKOMENDASI"}

        # {START "INI KALAU TIDAK ADA KORELASI REKOMENDASI"}
        else:
            text_2 = x.split()[0]
            recomend_sementara = df2[df2['Kode Awalan']
                                     == text_2]['produk'].values
            recomend_lain = df2['produk'].values

            n_recomend = 10

            condition = n_recomend - len(recomend_sementara)
            # {START "KALAU TERNYATA REKOMENDASI_SEMENTARA < 10 MAKA DITAMBAKAN DENGAN PRODUK ACAK"}
            if condition > 0:
                list_rekomendasi_lain = []
                for i in range(condition):
                    n_rekomendasi_lain = choice(recomend_lain)
                    list_rekomendasi_lain.append(n_rekomendasi_lain)
                recomend = np.concatenate(
                    (recomend_sementara, list_rekomendasi_lain))

            # {END "KALAU TERNYATA REKOMENDASI_SEMENTARA < 10 MAKA DITAMBAHKAN DENGAN PRODUK ACAK"}

            # {START "KALAU TERNYATA REKOMENDASI_SEMENTARA > 10 MAKA REKOMENDASI_SEMENTARA ADALAH SOLUSI"}
            else:
                recomend = recomend_sementara

            # {END "KALAU TERNYATA REKOMENDASI_SEMENTARA > MAKA REKOMENDASI_SEMENTARA ADALAH SOLUSI"}
        # {END "INI KALAU TIDAK ADA KORELASI REKOMENDASI"

        result = {'result': recomend}

    except:
        result = {'result': 'Terjadi Kesalahan'}

    return jsonify(result)


# inisiasi objeck flask
app = Flask(__name__)

# inisasi object flask_restful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# setup resource
# api.add_resource(Test, "/products", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run()
