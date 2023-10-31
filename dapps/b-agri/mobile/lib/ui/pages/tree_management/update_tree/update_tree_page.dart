import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/tree_management/update_tree/update_tree_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class UpdateTreePage extends StatefulWidget {
  final String? tree_id;
  final String? description;
  final String? name;

  UpdateTreePage({Key? key, this.tree_id, this.name, this.description})
      : super(key: key);

  @override
  _UpdateTreePageState createState() => _UpdateTreePageState();
}

class _UpdateTreePageState extends State<UpdateTreePage> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController nameController;
  late TextEditingController descriptionController;
  late UpdateTreeCubit _cubit;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _cubit = BlocProvider.of<UpdateTreeCubit>(context);
    _cubit.getTreeDetail(widget.tree_id!);

    nameController = TextEditingController();
    descriptionController = TextEditingController();

    _cubit.changeName(nameController.text);
    _cubit.changeDescription(descriptionController.text);

    nameController.addListener(() {
      _cubit.changeName(nameController.text);
    });

    descriptionController.addListener(() {
      _cubit.changeDescription(descriptionController.text);
    });
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
    _cubit.close();
    nameController.dispose();
    descriptionController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBarWidget(
        context: context,
        title: 'Chỉnh sửa thông tin cây trồng',
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Form(
                  key: _formKey,
                  child: BlocConsumer<UpdateTreeCubit, UpdateTreeState>(
                    listenWhen: (prev, current) =>
                        prev.loadStatus != current.loadStatus,
                    listener: (context, state) {
                      // TODO: implement listener
                      if (state.loadStatus == LoadStatus.SUCCESS) {
                        nameController.text = state.treeData!.name ?? "";
                        descriptionController.text =
                            state.treeData!.description ?? "";
                      }
                    },
                    builder: (context, state) {
                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Tên cây trồng',
                            style: AppTextStyle.greyS14,
                          ),
                          SizedBox(height: 10),
                          AppTextField(
                            hintText: '',
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
                      );
                    },
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
    return BlocConsumer<UpdateTreeCubit, UpdateTreeState>(
        bloc: _cubit,
        listenWhen: (prev, current) {
          return prev.updateTreeStatus != current.updateTreeStatus;
        },
        listener: (context, state) {
          if (state.updateTreeStatus == LoadStatus.SUCCESS) {
            _showCreateSuccess();
          }
          if (state.updateTreeStatus == LoadStatus.FAILURE) {
            showSnackBar('Có lỗi xảy ra!');
          }
        },
        builder: (context, state) {
          final isLoading = (state.updateTreeStatus == LoadStatus.LOADING);
          return Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Expanded(
                    child: AppButton(
                      color: AppColors.redButton,
                      title: 'Hủy bỏ',
                      onPressed: () {
                        Navigator.of(context).pop();
                      },
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
                          _cubit.updateTree(widget.tree_id);
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
    showSnackBar('Cập nhật thông tin thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}

class TreeUpdateArgument {
  String? tree_id;
  String? name;
  String? description;

  TreeUpdateArgument({
    this.tree_id,
    this.name,
    this.description,
  });
}
