import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/commons/screen_size.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/role/role_entity.dart';

import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';

import 'package:flutter_base/ui/components/app_button.dart';

import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_dropdown_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'login_cubit.dart';

class LoginPage extends StatefulWidget {
  LoginPage();

  @override
  State<StatefulWidget> createState() {
    return _LoginPageState();
  }
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  late StreamSubscription _navigationSubscription;
  late StreamSubscription _showMessageSubscription;

  final _usernameController = TextEditingController(text: '');
  final _passwordController = TextEditingController(text: '');

  final _scaffoldKey = GlobalKey<ScaffoldState>();

  LoginCubit? _cubit;

  @override
  void initState() {
    _cubit = BlocProvider.of<LoginCubit>(context);

    super.initState();

    _cubit!.changeRole(RoleEntity(role_id: "ktv", name: "Kỹ Thuật Viên"));

    _usernameController.addListener(() {
      _cubit!.usernameChange(_usernameController.text);
    });

    _passwordController.addListener(() {
      _cubit!.passChange(_passwordController.text);
    });

    _showMessageSubscription =
        _cubit!.showMessageController.stream.listen((event) {
      _showMessage(event);
    });

    _navigationSubscription =
        _cubit!.navigatorController.stream.listen((event) {
      switch (event) {
        case LoginNavigator.OPEN_HOME:
          showHome();
          break;
        case LoginNavigator.OPEN_GARDEN:
          showGardenManagementByQLV();
          break;
      }
    });
  }

  @override
  void dispose() {
    _cubit!.close();
    _usernameController.dispose();
    _passwordController.dispose();
    _showMessageSubscription.cancel();
    _navigationSubscription.cancel();
    super.dispose();
  }

  Future<bool> _onWillPop() async {
    showHome();
    return false;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        resizeToAvoidBottomInset: true,
        key: _scaffoldKey,
        backgroundColor: AppColors.background,
        body: _buildInput(),
      ),
    );
  }

  Widget _buildSignButton() {
    return BlocBuilder<LoginCubit, LoginState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return (prev.LoginStatus != current.LoginStatus) ||
            (prev.username != current.username) ||
            (prev.password != current.password);
      },
      builder: (context, state) {
        final isLoading = state.LoginStatus == LoginStatusBagri.LOADING;
        return Container(
          height: 40,
          margin: EdgeInsets.only(top: 31),
          padding: EdgeInsets.symmetric(horizontal: 28),
          child: AppButton(
            color: AppColors.main,
            width: double.infinity,
            title: S.of(context).sign_up_btn,
            textStyle: AppTextStyle.whiteS16Bold,
            onPressed: isLoading
                ? null
                : () {
                    if (_formKey.currentState!.validate()) {
                      _cubit!.signIn(state.username.trim(), state.password);
                    }
                  },
            isLoading: isLoading,
          ),
        );
      },
    );
  }

  void _showMessage(SnackBarMessage message) {
    _scaffoldKey.currentState!.removeCurrentSnackBar();
    _scaffoldKey.currentState!.showSnackBar(AppSnackBar(message: message));
  }

  Widget _buildInput() {
    return SingleChildScrollView(
      physics: ClampingScrollPhysics(),
      child: Form(
        key: _formKey,
        child: Column(
          children: [
            SizedBox(height: MediaQuery.of(context).size.height * 0.15),
            _buildLogo(),
            SizedBox(height: 8.15),
            _buildTextLabel(S.of(context).signIn_Username),
            _buildUserNameInput(),
            SizedBox(height: 3.37),
            _buildTextLabel(S.of(context).signIn_password),
            _buildPasswordInput(),
            // SizedBox(height: 3.37),
            // _buildTextLabel('Vai trò'),
            // _buildRoleOption(),
            SizedBox(height: 5),
            _buildTextForgotPass(),
            _buildSignButton(),
            SizedBox(height: 40),
            _buildTextRegistry(),
          ],
        ),
      ),
    );
  }

  Widget _buildTextLabel(String text) {
    return Container(
      alignment: Alignment.centerLeft,
      margin: EdgeInsets.symmetric(horizontal: 28),
      child: RichText(
        text: TextSpan(children: [
          TextSpan(
            text: text,
            style: AppTextStyle.blackS12,
          ),
        ]),
      ),
    );
  }

  Widget _buildUserNameInput() {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 28, vertical: 12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
      ),
      child: AppTextField(
        autoValidateMode: AutovalidateMode.onUserInteraction,
        hintText: 'Nhập vào tên người dùng',
        controller: _usernameController,
        validator: (value) {
          if (Validator.validateNullOrEmpty(value!))
            return "Chưa nhập tên người dùng";
          else
            return null;
        },
      ),
    );
  }

  Widget _buildPasswordInput() {
    return Container(
        margin: EdgeInsets.symmetric(horizontal: 28, vertical: 12),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(25.0),
        ),
        child: Stack(
          children: [
            AppTextField(
              autoValidateMode: AutovalidateMode.onUserInteraction,
              hintText: 'Nhập vào mật khẩu',
              keyboardType: TextInputType.visiblePassword,
              obscureText: true,
              controller: _passwordController,
              validator: (value) {
                if (Validator.validateNullOrEmpty(value!))
                  return "Chưa nhập mật khẩu";
                else
                  return null;
              },
            ),
          ],
        ));
  }

  Widget _buildRoleOption() {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 28, vertical: 12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
      ),
      child: AppRolePicker(
        onChange: (value) {
          _cubit!.changeRole(value);
        },
        value: RoleEntity(role_id: "ktv", name: "Kỹ Thuật Viên"),
        autoValidateMode: AutovalidateMode.onUserInteraction,
        validator: (value) {
          if (Validator.validateNullOrEmpty(value!.role_id!))
            return "Chưa chọn vai trò";
          else
            return null;
        },
      ),
    );
  }

  Widget _buildTextForgotPass() {
    return GestureDetector(
      onTap: () => {
        Application.router!.navigateTo(
          context,
          Routes.forgotPassword,
        )
      },
      child: Row(mainAxisAlignment: MainAxisAlignment.end, children: [
        Text(S.of(context).signIn_forgotPassword,
            style: TextStyle(
              fontSize: 11,
              color: Color(0xFF7A7A7A),
              fontStyle: FontStyle.italic,
            )),
        SizedBox(
          width: 30,
        )
      ]),
    );
  }

  Widget _buildTextRegistry() {
    return GestureDetector(
      onTap: () => {
        Application.router!.navigateTo(
          context,
          Routes.registry,
        )
      },
      child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text('Bạn chưa có tài khoản?',
            style: TextStyle(
              fontSize: 14,
              color: Color(0xFF000000),
            )),
        SizedBox(
          width: 5,
        ),
        Text('Đăng ký!',
            style: TextStyle(
              fontSize: 14,
              color: AppColors.main,
            )),
      ]),
    );
  }

  _buildLogo() {
    return Container(
      width: 180,
      height: 180,
      alignment: Alignment.center,
      child: Image.asset(AppImages.icBAgri, width: 180),
    );
  }

  void showHome() {
    final canPop = Navigator.of(context).canPop();
    if (canPop) {
      Application.router!.pop(context);
    } else {
      Application.router!.navigateTo(context, Routes.home, clearStack: true);
    }
  }

  void showGardenManagementByQLV() {
    final canPop = Navigator.of(context).canPop();
    if (canPop) {
      Application.router!.pop(context);
    } else {
      Application.router!
          .navigateTo(context, Routes.gardenListByQVL, clearStack: true);
    }
  }

  void _removeFocus() {
    FocusScope.of(context).requestFocus(FocusNode());
  }
}
