import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/ui/components/app_cache_image.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/season_detail_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:url_launcher/url_launcher.dart';

class QRCodeWidget extends StatefulWidget {
  String data;
  String nameSeason;
  String? linkQR;
  String? linkUrl;

  QRCodeWidget({
    Key? key,
    required this.data,
    required this.nameSeason,
    this.linkQR,
    this.linkUrl,
  }) : super(key: key);

  @override
  State<QRCodeWidget> createState() => _QRCodeWidgetState();
}

class _QRCodeWidgetState extends State<QRCodeWidget> {
  late SeasonDetailCubit _cubit;

  void initState() {
    _cubit = BlocProvider.of<SeasonDetailCubit>(context);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      clipBehavior: Clip.hardEdge,
      shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(20.0))),
      child: BlocBuilder<SeasonDetailCubit, SeasonDetailState>(
        builder: (context, state) {
          return Container(
            color: AppColors.main,
            padding: EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(widget.nameSeason,
                    style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w500,
                        color: Colors.white)),
                SizedBox(
                  height: 10,
                ),
                Container(
                  padding: EdgeInsets.all(10),
                  decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.all(Radius.circular(20.0))),
                  child: AppCacheImage(
                    url: state.linkQR,
                    width: 200,
                    height: 200,
                  ),
                ),
                SizedBox(
                  height: 10,
                ),
                GestureDetector(
                    onTap: () {
                      // _launchURL(widget.link!);
                      // print('state.linkQR ${state.linkQR}');
                      Clipboard.setData(ClipboardData(text: state.linkUrl));
                      showSnackBar('Đã sao chép');
                    },
                    child: Container(
                      padding: EdgeInsets.all(10),
                      decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius:
                              BorderRadius.all(Radius.circular(20.0))),
                      child: Text(
                        'Copylink',
                        style: TextStyle(
                          color: AppColors.main,
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    )),
              ],
            ),
          );
        },
      ),
    );
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}
