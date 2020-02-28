import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:health_card/App_pages/patient_doctor_login.dart';

class Home_page extends StatefulWidget {
  @override
  _Home_pageState createState() => _Home_pageState();
}

class _Home_pageState extends State<Home_page> {
  double screenHeight, screenWidth;
  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
    Size size = MediaQuery.of(context).size;
    screenHeight = size.height;
    screenWidth = size.width;
    return Scaffold(
        backgroundColor: Colors.white,
        body: Stack(
          children: <Widget>[
            Positioned(
              top: 0.20 * screenHeight,
              left: 0.32 * screenWidth,
              child: Container(
                height: 0.3 * screenHeight,
                width: 0.4 * screenWidth,
                child: Icon(
                  Icons.account_circle,
                  size: 0.4 * screenWidth,
                  color: Colors.blue,
                ),
              ),
            ),
            Positioned(
              top: 0.54 * screenHeight,
              left: 0.15 * screenWidth,
              child: Container(
                child: FlatButton(
                  color: Color(0xff5000aF),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Center(
                    child: Container(
                      height: 0.08 * screenHeight,
                      width: 0.6 * screenWidth,
                      child: Center(
                        child: Text(
                          "DOCTOR",
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ),
                  onPressed: () {
                    Navigator.pushNamed(context, patient_doctor_login.routeName,
                        arguments: "doctor");
                  },
                ),
              ),
            ),
            Positioned(
              top: 0.68 * screenHeight,
              left: 0.15 * screenWidth,
              child: Container(
                child: FlatButton(
                  color: Color(0xff5000aF),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Center(
                    child: Container(
                      height: 0.08 * screenHeight,
                      width: 0.6 * screenWidth,
                      child: Center(
                        child: Text(
                          "PATIENT",
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ),
                  onPressed: () {
                    Navigator.pushNamed(context, patient_doctor_login.routeName,
                        arguments: "patient");
                  },
                ),
              ),
            ),
          ],
        ));
  }
}
