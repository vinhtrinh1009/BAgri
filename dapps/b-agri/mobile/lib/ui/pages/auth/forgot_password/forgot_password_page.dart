import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/auth/forgot_password/forgot_password_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ForgotPasswordPage extends StatefulWidget {
  @override
  _ForgotPasswordPageState createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();
  ForgotPasswordCubit? _cubit;
  final _usernameController = TextEditingController(text: "");
  final _phoneController = TextEditingController(text: "");

  @override
  void initState() {
    _cubit = BlocProvider.of<ForgotPasswordCubit>(context);
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBarWidget(
        title: "Quên mật khẩu",
        context: context,
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
              child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 20),
            child: SingleChildScrollView(
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(
                      height: 27,
                    ),
                    Text(
                      'Tên đăng nhập',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      autoValidateMode: AutovalidateMode.onUserInteraction,
                      hintText: 'Nhập vào tên đăng nhập',
                      controller: _usernameController,
                      validator: (value) {
                        if (Validator.validateNullOrEmpty(value!))
                          return "Chưa nhập tên đăng nhập";
                        else
                          return null;
                      },
                    ),
                    SizedBox(
                      height: 27,
                    ),
                    Text(
                      'Số điện thoại',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      autoValidateMode: AutovalidateMode.onUserInteraction,
                      hintText: 'Nhập vào số điện thoại',
                      keyboardType: TextInputType.phone,
                      controller: _phoneController,
                      validator: (value) {
                        if (Validator.validateNullOrEmpty(value!)) {
                          return "Chưa nhập số điện thoại";
                        } else if (!Validator.validatePhone(value)) {
                          return "Số điện thoại không đúng định dạng";
                        } else
                          return null;
                      },
                    ),
                    SizedBox(
                      height: 50,
                    ),
                    _buildChangePassword(),
                  ],
                ),
              ),
            ),
          ))
        ],
      ),
    );
  }

  Widget _buildChangePassword() {
    return BlocConsumer<ForgotPasswordCubit, ForgotPasswordState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return (prev.loadStatus != current.loadStatus);
      },
      listener: (context, state) {
        if (state.loadStatus == LoadStatus.SUCCESS) {
          _showSuccess();
        }
        if (state.loadStatus == LoadStatus.FAILURE) {
          showSnackBar('Có lỗi xảy ra!');
        }
      },
      builder: (context, state) {
        final isLoading = state.loadStatus == LoadStatus.LOADING;
        return AppButton(
          width: double.infinity,
          title: 'Thay đổi mật khẩu',
          color: AppColors.main,
          isLoading: isLoading,
          onPressed: () {
            if (_formKey.currentState!.validate()) {
              _cubit!.forgotPassword(
                  _usernameController.text, _phoneController.text);
            }
          },
        );
      },
    );
  }

  void _showSuccess() async {
    showSnackBar('Reset mật khẩu thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}
