import 'package:fluro/fluro.dart';
import 'package:flutter/material.dart';

/// Root
Handler notHandler = new Handler(
  handlerFunc: (BuildContext? context, Map<String, List<String>> params) =>
      Scaffold(
    body: Center(
      child: Text('$params'),
    ),
  ),
);
