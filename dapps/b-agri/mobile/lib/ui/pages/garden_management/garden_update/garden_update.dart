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

import 'garden_update_cubit.dart';

class UpdateGardenPage extends StatefulWidget {
  final String? garden_id;
  final String? name;
  final int? area;

  const UpdateGardenPage({
    this.garden_id,
    this.name,
    this.area,
  });

  @override
  _UpdateGardenPageState createState() => _UpdateGardenPageState();
}

class _UpdateGardenPageState extends State<UpdateGardenPage> {
  late TextEditingController nameController;
  late TextEditingController areaController;
  GardenUpdateCubit? _cubit;

  final _scaffoldKey = GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();

    _cubit = BlocProvider.of<GardenUpdateCubit>(context);

    //Set initial cubit
    _cubit!.fetchGardenDetail(widget.garden_id);

    nameController = TextEditingController();
    areaController = TextEditingController();

    _cubit!.changeName(nameController.text);
    _cubit!.changeArea(areaController.text);

    nameController.addListener(() {
      _cubit!.changeName(nameController.text);
    });

    areaController.addListener(() {
      _cubit!.changeArea(areaController.text);
    });
  }

  @override
  void dispose() {
    _cubit!.close();
    nameController.dispose();
    areaController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBarWidget(
        title: 'Chỉnh sửa thông tin vườn',
        context: context,
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          SizedBox(height: 26),
          Expanded(flex: 4, child: _buildBodyWidget(context)),
          Expanded(flex: 1, child: _buildEditButton()),
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
              child: BlocConsumer<GardenUpdateCubit, GardenUpdateState>(
                listenWhen: (prev, current) =>
                    prev.detailGardenStatus != current.detailGardenStatus,
                listener: (context, state) {
                  // TODO: implement listener
                  if (state.detailGardenStatus == LoadStatus.SUCCESS) {
                    nameController.text = state.gardenData!.name ?? "";
                    areaController.text = state.gardenData!.area.toString();
                  }
                },
                builder: (context, state) {
                  return Padding(
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
                          enable: state.editGardenStatus == LoadStatus.LOADING
                              ? false
                              : true,
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
                          enable: state.editGardenStatus == LoadStatus.LOADING
                              ? false
                              : true,
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
                          managerId:
                              state.detailGardenStatus == LoadStatus.SUCCESS
                                  ? state.gardenData!.manager!.manager_id
                                  : null,
                          onChange: state.detailGardenStatus ==
                                  LoadStatus.LOADING
                              ? null
                              : (value) {
                                  _cubit!
                                      .changeManagerId(value!.manager_id ?? "");
                                },
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            color: Colors.white,
          ),
        ],
      ),
    );
  }

  Widget _buildEditButton() {
    return BlocConsumer<GardenUpdateCubit, GardenUpdateState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return prev.editGardenStatus != current.editGardenStatus;
      },
      listener: (context, state) {
        if (state.editGardenStatus == LoadStatus.SUCCESS) {
          _showCreateSuccess();
        }
        if (state.editGardenStatus == LoadStatus.FAILURE) {
          showSnackBar('Có lỗi xảy ra!');
        }
      },
      builder: (context, state) {
        final isLoading = (state.editGardenStatus == LoadStatus.LOADING);
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
                    _cubit!.updateGarden(widget.garden_id);
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
    showSnackBar('Cập nhật thông tin vườn thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}

class GardenUpdateArgument {
  String? garden_id;
  String? name;
  int? area;

  GardenUpdateArgument({
    this.garden_id,
    this.name,
    this.area,
  });
}
