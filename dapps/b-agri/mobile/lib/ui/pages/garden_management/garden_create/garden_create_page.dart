import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/components/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/ui/widgets/b_agri/drop_down_picker/app_manager_picker.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'garden_create_cubit.dart';

class CreateGardenPage extends StatefulWidget {
  @override
  _CreateGardenPageState createState() => _CreateGardenPageState();
}

class _CreateGardenPageState extends State<CreateGardenPage> {
  final _formKey = GlobalKey<FormState>();
  final nameController = TextEditingController(text: "");
  final areaController = TextEditingController(text: "");
  late GardenCreateCubit _cubit;
  String managerId = "";

  final _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();

    _cubit = BlocProvider.of<GardenCreateCubit>(context);

    //Set initial cubit
    _cubit.changeName(nameController.text);
    _cubit.changeArea(areaController.text);

    nameController.addListener(() {
      _cubit.changeName(nameController.text);
    });

    areaController.addListener(() {
      _cubit.changeArea(areaController.text);
    });
  }

  @override
  void dispose() {
    _cubit.close();
    nameController.dispose();
    areaController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBarWidget(
        title: 'Thêm mới vườn',
        context: context,
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          SizedBox(height: 26),
          Expanded(flex: 4, child: _buildBodyWidget(context)),
          Expanded(flex: 1, child: _buildCreateButton()),
        ],
      ),
    );
  }

  Widget _buildBodyWidget(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: <Widget>[
          SizedBox(height: 17),
          Container(
            child: Form(
              key: _formKey,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 30),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Tên vườn',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      autoValidateMode: AutovalidateMode.onUserInteraction,
                      hintText: 'Nhập vào tên vườn',
                      controller: nameController,
                      validator: (value) {
                        if (Validator.validateNullOrEmpty(value!))
                          return "Chưa nhập tên vườn";
                        else
                          return null;
                      },
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Diện tích',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      hintText: 'Nhập vào diện tích',
                      controller: areaController,
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Người quản lý',
                      style: AppTextStyle.greyS14,
                    ),
                    SizedBox(height: 10),
                    AppManagerPicker(
                      onChange: (value) {
                        _cubit.changeManagerId(value!.manager_id ?? "");
                      },
                    ),
                  ],
                ),
              ),
            ),
            color: Colors.white,
          ),
        ],
      ),
    );
  }

  Widget _buildCreateButton() {
    return BlocConsumer<GardenCreateCubit, GardenCreateState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return prev.createGardenStatus != current.createGardenStatus;
      },
      listener: (context, state) {
        if (state.createGardenStatus == LoadStatus.SUCCESS) {
          _showCreateSuccess();
        }
        if (state.createGardenStatus == LoadStatus.FAILURE) {
          showSnackBar('Có lỗi xảy ra!');
        }
      },
      builder: (context, state) {
        final isLoading = (state.createGardenStatus == LoadStatus.LOADING);
        return Container(
          margin: const EdgeInsets.symmetric(horizontal: 60),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                flex: 1,
                child: AppRedButton(
                  title: 'Hủy bỏ',
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ),
              SizedBox(
                width: 30,
              ),
              Expanded(
                flex: 1,
                child: AppGreenButton(
                  title: 'Xác nhận',
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      _cubit.createGarden();
                    }
                  },
                  isLoading: isLoading,
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _showCreateSuccess() async {
    showSnackBar('Tạo mới vườn thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}
