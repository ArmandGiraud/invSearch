import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tf_sentencepiece
import os
import json
from sklearn.metrics.pairwise import cosine_similarity


class TermsSearch():
    def __init__(self, suggest_dict_path, stops_path):
        self.load_suggest_dict(suggest_dict_path)
        self.load_stops(stops_path)

        self.build_answers()

    def load_suggest_dict(self, suggest_dict_path):
        with open(suggest_dict_path) as f:
            self.suggest_dict = json.load(f)


    def load_stops(self, stops_path):

        with open(stops_path) as f:
            stops = f.read().splitlines()

        stops.extend(["travail", "travailler"])
        self.stops = set(stops)

    def remove_stops(self, string: str):
        tokens = string.split()
        tokens_filtered = [
            t for t in tokens if t not in self.stops ]
        return " ".join(tokens_filtered)

    def build_answers(self):
        g = tf.Graph()
        with g.as_default():
            self.q_placeholder = tf.placeholder(tf.string, shape = [None])
            self.r_placeholder = tf.placeholder(tf.string, shape = [None])
            self.c_placeholder = tf.placeholder(tf.string, shape = [None])
            module = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/1", trainable=True)
            self.question_embeddings = module(
                                        dict(input=self.q_placeholder),
                                        signature="question_encoder", as_dict=True)

            response_embeddings = module(
                                        dict(input=self.r_placeholder,
                                            context=self.c_placeholder),
                                        signature="response_encoder", as_dict=True)
            init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
        g.finalize()

        self.session = tf.Session(graph=g)
        self.session.run(init_op)

        self.res = self.session.run(response_embeddings, {self.r_placeholder: [self.remove_stops(k) for k in self.suggest_dict],
                                                    self.c_placeholder: ["" for k in self.suggest_dict]})

    def predict_use_terms(self, query, n=10):
        query = self.remove_stops(query)
        questions = [query.lower()]
        question_results = self.session.run(
                self.question_embeddings, {self.q_placeholder: questions})

        topn = cosine_similarity(self.res["outputs"], question_results["outputs"].reshape(1, -1)).squeeze().argsort()[::-1][:n]
        return [self.suggest_dict[t] for t in topn]


if __name__ == "__main__":
    ts = TermsSearch("suggest_dict.json", "stops.txt")
    print(ts.predict_use_terms("je pars en vacances"))
    