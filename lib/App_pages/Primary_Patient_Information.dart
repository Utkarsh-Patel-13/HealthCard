import 'package:flutter/material.dart';
import 'package:qrscan/qrscan.dart' as scanner;

class Primary_Patient_Information extends StatefulWidget {
  @override
  _Primary_Patient_InformationState createState() =>
      _Primary_Patient_InformationState();
}

class _Primary_Patient_InformationState
    extends State<Primary_Patient_Information> {
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
