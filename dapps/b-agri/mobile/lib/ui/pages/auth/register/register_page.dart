import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/role/role_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/components/app_button.dart';
import 'package:flutter_base/ui/pages/auth/register/registry_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_dropdown_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class RegistryPage extends StatefulWidget {
  RegistryPage();

  @override
  State<StatefulWidget> createState() {
    return _RegistryPageState();
  }
}

class _RegistryPageState extends State<RegistryPage> {
  final _formKey = GlobalKey<FormState>();

  final _usernameController = TextEditingController(text: '');
  final _passwordController = TextEditingController(text: '');
  final _phoneController = TextEditingController(text: '');
  final _fullNameController = TextEditingController(text: '');
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  bool isErrorMessage = false;
  RegistryCubit? _cubit;
  bool isFirst = false;

  @override
  void initState() {
    _cubit = BlocProvider.of<RegistryCubit>(context);

    super.initState();

    _cubit!.changeRole(RoleEntity(role_id: "ktv", name: "Kỹ Thuật Viên"));

    _usernameController.addListener(() {
      _cubit!.usernameChange(_usernameController.text);
    });

    _passwordController.addListener(() {
      _cubit!.passChange(_passwordController.text);
    });

    _phoneController.addListener(() {
      _cubit!.changePhone(_phoneController.text);
    });

    _fullNameController.addListener(() {
      _cubit!.changeFullName(_fullNameController.text);
    });
  }

  @override
  void dispose() {
    _cubit!.close();
    _usernameController.dispose();
    _passwordController.dispose();
    _phoneController.dispose();
    _fullNameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        resizeToAvoidBottomInset: true,
        key: _scaffoldKey,
        backgroundColor: AppColors.background,
        appBar: AppBarWidget(
          title: 'Đăng ký',
          context: context,
        ),
        body: SafeArea(
            child: Column(
          children: [
            _buildInput(),
            _buildRegisterButton(),
            SizedBox(height: 10),
          ],
        )),
      ),
    );
  }

  Widget _buildInput() {
    return Expanded(
      child: Scrollbar(
        isAlwaysShown: true,
        child: SingleChildScrollView(
          physics: ClampingScrollPhysics(),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                _buildLogo(),
                SizedBox(height: 20.15),
                _buildTextLabel(S.of(context).signIn_Username),
                _buildUserNameInput(),
                SizedBox(height: 3),
                _buildTextLabel(S.of(context).signIn_password),
                _buildPasswordInput(),
                SizedBox(height: 3),
                _buildTextLabel('Họ và tên'),
                _buildFullNameInput(),
                SizedBox(height: 3),
                _buildTextLabel('Số điện thoại'),
                _buildPhoneInput(),
                SizedBox(height: 3),
                _buildTextLabel('Vai trò'),
                _buildRoleOption(),
                SizedBox(height: 5),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRegisterButton() {
    return BlocConsumer<RegistryCubit, RegistryState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return (prev.RegisterStatus != current.RegisterStatus);
      },
      listener: (context, state) {
        if (state.RegisterStatus == LoadStatus.SUCCESS) {
          _showCreateSuccess();
        }
        if (state.RegisterStatus == LoadStatus.FAILURE) {
          showSnackBar('${state.messageError}');
        }
      },
      builder: (context, state) {
        final isLoading = state.RegisterStatus == LoadStatus.LOADING;
        if (isErrorMessage) {
          return SizedBox(
            height: 40,
          );
        }
        return Container(
          height: 40,
          width: double.infinity,
          margin: EdgeInsets.only(top: 25),
          padding: EdgeInsets.symmetric(horizontal: 28),
          child: AppButton(
            title: 'Đăng ký',
            textStyle: AppTextStyle.whiteS16Bold,
            onPressed: isLoading
                ? null
                : () {
                    if (_formKey.currentState!.validate()) {
                      _cubit!.registry(
                          _usernameController.text,
                          _passwordController.text,
                          _fullNameController.text,
                          _phoneController.text,
                          state.role!.role_id!);
                    }
                  },
            isLoading: isLoading,
            color: AppColors.main,
          ),
        );
      },
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

  Widget _buildFullNameInput() {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 28, vertical: 12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
      ),
      child: AppTextField(
        autoValidateMode: AutovalidateMode.onUserInteraction,
        hintText: 'Nhập vào tên đẩy đủ',
        controller: _fullNameController,
        validator: (value) {
          if (Validator.validateNullOrEmpty(value!))
            return "Chưa nhập tên đẩy đủ";
          else
            return null;
        },
      ),
    );
  }

  Widget _buildPhoneInput() {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 28, vertical: 12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
      ),
      child: AppTextField(
        autoValidateMode: AutovalidateMode.onUserInteraction,
        hintText: 'Nhập vào số điện thoại',
        keyboardType: TextInputType.number,
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
    );
  }

  Widget _buildPasswordInput() {
    return Container(
        margin: EdgeInsets.symmetric(horizontal: 28, vertical: 12),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10.0),
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
        borderRadius: BorderRadius.circular(10.0),
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

  _buildLogo() {
    return Container(
      width: 180,
      height: 180,
      alignment: Alignment.center,
      child: Image.asset(AppImages.icBAgri, width: 180),
    );
  }

  void _showCreateSuccess() async {
    showSnackBar('Đăng ký thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) async {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
    setState(() {
      isErrorMessage = true;
    });
    await Future.delayed(Duration(milliseconds: 2200));
    setState(() {
      isErrorMessage = false;
    });
  }
}
