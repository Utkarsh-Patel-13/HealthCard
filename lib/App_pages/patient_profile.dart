import 'package:flutter/material.dart';
import 'package:health_card/Models/patient_model.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:health_card/App_pages/patient_navigation.dart';

class Profile_Page extends StatefulWidget {
  var aadharno;
  Profile_Page(this.aadharno);
  @override
  _Profile_PageState createState() => _Profile_PageState(aadharno);
}

class _Profile_PageState extends State<Profile_Page> {
  _Profile_PageState(this.aadharno);
  var decodejson;
  var body;
  var aadharno;
  Patient_Model pm;
  void pm_change(var name, var aadhar, var gen, var add, var dob, var emal,
      var conno, var emrcon) {
    pm = Patient_Model(name, emal, conno, gen, aadhar, add, dob, emrcon);
  }

  Future profile_get() async {
    http.Response response = await http.get(
        "http://192.168.43.212:3000/patient/profile/" + aadharno,
        headers: {"Accept": "application.json"});
    print(response.body);
    //return response.body;
    decodejson = jsonDecode(response.body);
    setState(() {
      pm_change(
          decodejson['Name'],
          decodejson['AadharNo'],
          decodejson['Gender'],
          decodejson['Address'],
          decodejson['DOB'],
          decodejson['Email'],
          decodejson['ContactNo'],
          decodejson['EmergencyContact']);
    });
  }

  @override
  void initState() {
    profile_get();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          SizedBox(
            height: 18,
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(pm.Name.toString(), style: TextStyle(fontSize: 20)),
          ),
          SizedBox(
            height: 18,
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(pm.DOB.toString(), style: TextStyle(fontSize: 20)),
          ),
          SizedBox(
            height: 18,
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(pm.Gender.toString(), style: TextStyle(fontSize: 20)),
          ),
          SizedBox(
            height: 18,
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(pm.AadharNo.toString(), style: TextStyle(fontSize: 20)),
          ),
          SizedBox(
            height: 18,
          ),
          Row(
            children: <Widget>[
              Icon(
                Icons.phone,
                color: Colors.blue,
              ),
              Text(pm.ContactNo.toString(), style: TextStyle(fontSize: 20)),
            ],
          ),
          SizedBox(
            height: 18,
          ),
          Row(
            children: <Widget>[
              Icon(
                Icons.email,
                color: Colors.blue,
              ),
              Text(pm.Email.toString(), style: TextStyle(fontSize: 20)),
            ],
          ),
          SizedBox(
            height: 18,
          ),
          Row(
            children: <Widget>[
              Icon(
                Icons.contact_phone,
                color: Colors.blue,
              ),
              Text(pm.EmergencyContact.toString(),
                  style: TextStyle(fontSize: 20)),
            ],
          ),
          SizedBox(
            height: 18,
          ),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: <Widget>[
                Icon(
                  Icons.location_on,
                  color: Colors.blue,
                ),
                Text(
                  pm.Address.toString(),
                  style: TextStyle(fontSize: 20),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
