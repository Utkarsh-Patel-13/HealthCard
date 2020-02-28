import 'package:flutter/material.dart';
import 'package:qrscan/qrscan.dart' as scanner;
import 'package:health_card/App_pages/patient_navigation.dart';
import 'package:http/http.dart' as http;

class Give_Access extends StatefulWidget {
  var aadharno;
  Give_Access(this.aadharno);
  @override
  _Give_AccessState createState() => _Give_AccessState(aadharno);
}

class _Give_AccessState extends State<Give_Access> {
  var aadharno;
  _Give_AccessState(this.aadharno);
  var scanned = "Please Scan QR";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.yellow,
      body: Column(
        children: <Widget>[
          SizedBox(
            height: 200,
          ),
          Center(
            child: Text(scanned),
          ),
          Center(
            child: FlatButton(
              child: Text(
                "scan",
                style: TextStyle(fontSize: 28),
              ),
              onPressed: () async {
                var cameraScanResult = await scanner.scan();
                http.patch("http://192.168.43.212:3000/patient/access/" +
                    aadharno +
                    "-" +
                    cameraScanResult);
                setState(() {
                  this.scanned = cameraScanResult;
                });
              },
            ),
          )
        ],
      ),
    );
  }
}
