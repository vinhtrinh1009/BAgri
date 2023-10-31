import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/generated/l10n.dart';

class ErrorListWidget extends StatelessWidget {
  final String? text;
  final RefreshCallback? onRefresh;

  ErrorListWidget({
    this.text,
    this.onRefresh,
  });

  @override
  Widget build(BuildContext context) {
    // return Center(
    //   child: Container(
    //     child: RefreshIndicator(
    //         child: ListView.builder(
    //           itemBuilder: (context, index) {
    //             return Container(
    //               height: height ?? MediaQuery.of(context).size.height * 0.85,
    //               width: double.infinity,
    //               child: Center(
    //                 child: Text(
    //                   text ?? S.of(context).common_fetchDataFailure,
    //                 ),
    //               ),
    //             );
    //           },
    //           itemCount: 1,
    //         ),
    //         onRefresh: onRefresh),
    //   ),
    // );
    return Stack(
      children: [
        Center(
          child: Text(
            text ?? S.of(context).common_fetchDataFailure,
          ),
        ),
        RefreshIndicator(
            child: ListView.builder(
              itemBuilder: (context, index) {
                return Center(
                  child: Container(),
                );
              },
              itemCount: 1,
            ),
            onRefresh: onRefresh!)
      ],
    );
  }
}
