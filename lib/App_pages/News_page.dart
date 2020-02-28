import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class News extends StatefulWidget {
  @override
  _NewsState createState() => _NewsState();
}

class _NewsState extends State<News> {
  var news_list = new List(100);
  var json = "hello";
  Future<String> getNews() async {
    http.Response response = await http.get('http://192.168.43.212:3000/news/',
        headers: {"Accept": "application/json"});
    print(response.body);
    var decodeJson = jsonDecode(response.body);
    setState(() {
      json = decodeJson;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.pink,
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            ListView(
              children: <Widget>[
                Text(json),
              ],
            )
          ],
        ),
      ),
    );
  }
}
