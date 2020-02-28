import 'package:flutter/material.dart';

class Patient_Model {
  String Name;
  String Email;
  String Gender;
  String AadharNo;
  String DOB;
  String Address;
  String ContactNo;
  String EmergencyContact;

  Patient_Model(this.Name, this.Email, this.ContactNo, this.Gender,
      this.AadharNo, this.Address, this.DOB, this.EmergencyContact);
}
