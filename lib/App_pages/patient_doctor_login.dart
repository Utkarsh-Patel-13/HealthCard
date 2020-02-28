import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:health_card/http_requests/login_http.dart';

class patient_doctor_login extends StatefulWidget {
  static const routeName = '/patient_doctor_login';

  @override
  _patient_doctor_loginState createState() => _patient_doctor_loginState();
}

class logins {
  String Email;
  String Password;
}

//final _formKey = GlobalKey<FormState>();

class _patient_doctor_loginState extends State<patient_doctor_login>
    with SingleTickerProviderStateMixin {
  double screenWidth, screenHeight;
  var pass;
  final emailController = TextEditingController();

  final passwordController = TextEditingController();

  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    logins l = logins();
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
    Size size = MediaQuery.of(context).size;
    screenHeight = size.height;
    screenWidth = size.width;
    var selected = ModalRoute.of(context).settings.arguments;
    return Scaffold(
      body: Container(
        child: Stack(
          children: <Widget>[
            Container(
              child: Column(
                children: <Widget>[
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [
                            const Color(0xff1300FF),
                            const Color(0xff5f00DF),
                          ],
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                      ),
                    ),
                  )
                ],
              ),
            ),
            Positioned(
              top: 0.4 * screenHeight,
              left: 0.1 * screenWidth,
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  boxShadow: [
                    BoxShadow(
                        color: Color(0xffc8c8c8),
                        blurRadius: 0.2,
                        spreadRadius: 1.7,
                        offset: Offset(
                          0.1,
                          2.0,
                        )),
                  ],
                  borderRadius: BorderRadius.circular(18),
                ),
                child: SizedBox(
                  height: 0.4 * screenHeight,
                  width: 0.8 * screenWidth,
                  child: form(context),
                ),
              ),
            ),
            Positioned(
              top: 0.76 * screenHeight,
              left: 0.25 * screenWidth,
              child: Container(
                child: FlatButton(
                  color: Color(0xff1300FF),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Center(
                    child: Container(
                      height: 0.07 * screenHeight,
                      width: 0.4 * screenWidth,
                      child: Center(
                        child: Text(
                          "LOGIN",
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ),
                  onPressed: () {
                    l.Email = emailController.text;
                    l.Password = passwordController.text;
                    if (l.Email != null && l.Password != null) {
                      login(l.Email, l.Password, selected, context);
                    }
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Form form(BuildContext context) {
    return Form(
      //key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Center(
            child: Text(
              "LOGIN",
              style: TextStyle(
                fontSize: 17,
                color: Colors.grey,
              ),
            ),
          ),
          SizedBox(
            height: 0.07,
          ),
          Text(
            "      EMAIL",
            style: TextStyle(
              fontSize: 12,
              color: Colors.blue[900],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(25, 0, 25, 0),
            child: TextFormField(
              textAlign: TextAlign.left,
              controller: emailController,
              decoration: const InputDecoration(hintText: 'Email'),
              validator: (value) {
                if (value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
          SizedBox(
            height: 0.07 * screenHeight,
          ),
          Text(
            "      PASSWORD",
            style: TextStyle(
              fontSize: 12,
              color: Colors.blue[900],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(25, 0, 25, 0),
            child: TextFormField(
              textAlign: TextAlign.left,
              controller: passwordController,
              decoration: const InputDecoration(hintText: 'Password'),
              obscureText: true,
              validator: (value) {
                if (value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );
  }
}
