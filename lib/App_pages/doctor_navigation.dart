import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:health_card/App_pages/doctor_profile.dart';
import 'package:health_card/App_pages/Primary_Patient_Information.dart';
import 'package:health_card/App_pages/News_page.dart';
import 'package:health_card/main.dart';

class Doctor_Navigation extends StatefulWidget {
  static const routeName = '/doctor_navigation';
  @override
  _Doctor_NavigationState createState() => _Doctor_NavigationState();
}

class _Doctor_NavigationState extends State<Doctor_Navigation> {
  int doc_nav_index = 0;
  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
    String aadharno = ModalRoute.of(context).settings.arguments;
    return Scaffold(
      appBar: AppBar(
        title: Text("Health Card"),
      ),
      backgroundColor: Colors.white,
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.pink,
              ),
              child: Text("Health Card"),
            ),
            ListTile(
              title: Text("Profile"),
              onTap: () {
                setState(() {
                  doc_nav_index = 0;
                });
                Navigator.pop(context);
              },
            ),
            ListTile(
              title: Text("Primary Patient Information"),
              onTap: () {
                setState(() {
                  doc_nav_index = 1;
                });
                Navigator.pop(context);
              },
            ),
            SizedBox(
              height: 160,
            ),
            ListTile(
              title: Text(
                "Logout",
                style: TextStyle(color: Colors.black),
              ),
              onTap: () {
                Navigator.of(context).pushAndRemoveUntil(
                    MaterialPageRoute(builder: (context) => MyApp()),
                    (Route<dynamic> route) => false);
              },
            ),
          ],
        ),
      ),
      body: IndexedStack(
        index: doc_nav_index,
        children: <Widget>[
          Profile_page(aadharno),
          Primary_Patient_Information(),
        ],
      ),
    );
  }
}
