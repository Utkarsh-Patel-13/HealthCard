import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:health_card/App_pages/patient_profile.dart';
import 'package:health_card/App_pages/News_page.dart';
import 'package:health_card/App_pages/Give_Access.dart';
import 'package:health_card/main.dart';

class Patient_Navigation extends StatefulWidget {
  static const routeName = '/patient_navigation';
  @override
  _Patient_NavigationState createState() => _Patient_NavigationState();
}

class _Patient_NavigationState extends State<Patient_Navigation> {
  int pat_nav_index = 0;
  @override
  Widget build(BuildContext context) {
    String aadharno = ModalRoute.of(context).settings.arguments;
    return Scaffold(
      appBar: AppBar(
        title: Text("Health Card"),
      ),
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
                  pat_nav_index = 0;
                });
                Navigator.pop(context);
              },
            ),
            ListTile(
              title: Text("Give Access"),
              onTap: () {
                setState(() {
                  pat_nav_index = 1;
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
        index: pat_nav_index,
        children: <Widget>[
          Profile_Page(aadharno),
          Give_Access(aadharno),
        ],
      ),
    );
  }
}
