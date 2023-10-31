import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/auth/change_password/change_password_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ChangePasswordPage extends StatefulWidget {
  @override
  _ChangePasswordPageState createState() => _ChangePasswordPageState();
}

class _ChangePasswordPageState extends State<ChangePasswordPage> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();

  ChangePasswordCubit? _cubit;

  final _oldPasswordController = TextEditingController(text: "");
  final _newPasswordController = TextEditingController(text: "");
  final _confirmNewPasswordController = TextEditingController(text: "");

  @override
  void initState() {
    _cubit = BlocProvider.of<ChangePasswordCubit>(context);
  }

  @override
  void dispose() {
    _oldPasswordController.dispose();
    _newPasswordController.dispose();
    _confirmNewPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBarWidget(
        title: "Đổi mật khẩu",
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
                      'Mật khẩu',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      autoValidateMode: AutovalidateMode.onUserInteraction,
                      hintText: 'Nhập vào mật khẩu',
                      keyboardType: TextInputType.visiblePassword,
                      obscureText: true,
                      controller: _oldPasswordController,
                      validator: (value) {
                        if (Validator.validateNullOrEmpty(value!))
                          return "Chưa nhập mật khẩu";
                        else
                          return null;
                      },
                    ),
                    SizedBox(
                      height: 27,
                    ),
                    Text(
                      'Mật khẩu mới',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      autoValidateMode: AutovalidateMode.onUserInteraction,
                      hintText: 'Nhập vào mật khẩu mới',
                      keyboardType: TextInputType.visiblePassword,
                      obscureText: true,
                      controller: _newPasswordController,
                      validator: (value) {
                        if (Validator.validateNullOrEmpty(value!))
                          return "Chưa nhập mật khẩu mới";
                        else {
                          if (value == _oldPasswordController.text) {
                            return "Không được trùng mật khẩu cũ";
                          } else {
                            return null;
                          }
                        }
                      },
                    ),
                    SizedBox(
                      height: 27,
                    ),
                    Text(
                      'Xác nhận mật khẩu mới',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      autoValidateMode: AutovalidateMode.onUserInteraction,
                      hintText: 'Nhập vào mật khẩu mới',
                      keyboardType: TextInputType.visiblePassword,
                      obscureText: true,
                      controller: _confirmNewPasswordController,
                      validator: (value) {
                        if (Validator.validateNullOrEmpty(value!))
                          return "Chưa nhập mật khẩu mới";
                        else {
                          if (value != _newPasswordController.text) {
                            return "Mật khẩu mới không trùng khớp";
                          } else {
                            return null;
                          }
                        }
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
    return BlocConsumer<ChangePasswordCubit, ChangePasswordState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return (prev.loadStatus != current.loadStatus);
      },
      listener: (context, state) {
        if (state.loadStatus == LoadStatus.SUCCESS) {
          _showCreateSuccess();
          _cubit!.removeUserSection();
          Application.router!.navigateTo(context, Routes.login,
              clearStack: true, replace: true);
        }
        if (state.loadStatus == LoadStatus.FAILURE) {
          showSnackBar('Có lỗi xảy ra!');
        }
      },
      builder: (context, state) {
        final isLoading = state.loadStatus == LoadStatus.LOADING;
        return AppButton(
          width: double.infinity,
          color: AppColors.main,
          isLoading: isLoading,
          title: 'Thay đổi mật khẩu',
          onPressed: () {
            if (_formKey.currentState!.validate()) {
              _cubit!.changePassword(
                  _oldPasswordController.text,
                  _newPasswordController.text,
                  _confirmNewPasswordController.text);
            }
          },
        );
      },
    );
  }

  void _showCreateSuccess() async {
    showSnackBar('Đổi mật khẩu thành công.Vui lòng đăng nhập lại!');
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}
