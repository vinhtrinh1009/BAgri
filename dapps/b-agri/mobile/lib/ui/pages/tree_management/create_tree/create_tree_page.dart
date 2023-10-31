import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/tree_management/create_tree/create_tree_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class CreateTreePage extends StatefulWidget {
  const CreateTreePage({Key? key}) : super(key: key);

  @override
  _CreateTreePageState createState() => _CreateTreePageState();
}

class _CreateTreePageState extends State<CreateTreePage> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController nameController;
  late TextEditingController descriptionController;
  CreateTreeCubit? _cubit;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    nameController = TextEditingController();
    descriptionController = TextEditingController();

    _cubit = BlocProvider.of<CreateTreeCubit>(context);
    //Set initial cubit
    nameController.addListener(() {
      _cubit!.changeName(nameController.text);
    });
    descriptionController.addListener(() {
      _cubit!.changeDescription(descriptionController.text);
    });
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
    _cubit!.close();
    nameController.dispose();
    descriptionController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBarWidget(
        context: context,
        title: 'Thêm cây trồng',
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 15, vertical: 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Tên cây trồng',
                        style: AppTextStyle.greyS14,
                      ),
                      SizedBox(height: 10),
                      AppTextField(
                        autoValidateMode: AutovalidateMode.onUserInteraction,
                        hintText: 'Tên cây trồng',
                        controller: nameController,
                        validator: (value) {
                          if (Validator.validateNullOrEmpty(value!))
                            return "Chưa nhập tên cây trồng";
                          else
                            return null;
                        },
                      ),
                      SizedBox(height: 20),
                      Text(
                        'Mô tả',
                        style: AppTextStyle.greyS14,
                      ),
                      SizedBox(height: 10),
                      AppTextAreaField(
                        hintText: '',
                        maxLines: 8,
                        controller: descriptionController,
                      ),
                    ],
                  ),
                ),
                SizedBox(
                  height: 40,
                ),
                buildActionCreate(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget buildActionCreate() {
    return BlocConsumer<CreateTreeCubit, CreateTreeState>(
        bloc: _cubit,
        listenWhen: (prev, current) {
          return prev.createTreeStatus != current.createTreeStatus;
        },
        listener: (context, state) {
          if (state.createTreeStatus == LoadStatus.SUCCESS) {
            _showCreateSuccess();
          }
          if (state.createTreeStatus == LoadStatus.FAILURE) {
            showSnackBar('Có lỗi xảy ra!');
          }
        },
        builder: (context, state) {
          final isLoading = (state.createTreeStatus == LoadStatus.LOADING);
          return Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Expanded(
                    child: AppButton(
                      color: AppColors.redButton,
                      title: 'Hủy bỏ',
                    ),
                  ),
                  SizedBox(width: 40),
                  Expanded(
                    child: AppButton(
                      width: 100,
                      color: AppColors.main,
                      title: 'Xác nhận',
                      onPressed: () {
                        if (_formKey.currentState!.validate()) {
                          _cubit?.createTree();
                        }
                      },
                      isLoading: isLoading,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 90),
            ],
          );
        });
  }

  void _showCreateSuccess() async {
    showSnackBar('Tạo mới thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}
