import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/garden_picker/app_garden_picker_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_html/shims/dart_ui.dart';

import '../../app_button.dart';
import '../../app_circular_progress_indicator.dart';

class AppProcessPickerPage extends StatefulWidget {
  final String? selectedProcessId;
  final String? selectedTreeId;

  AppProcessPickerPage({this.selectedProcessId, this.selectedTreeId});

  @override
  _AppProcessPickerPageState createState() => _AppProcessPickerPageState();
}

class _AppProcessPickerPageState extends State<AppProcessPickerPage> {
  late AppCubit _cubit;
  ProcessEntity? selectedGarden;

  @override
  void initState() {
    _cubit = BlocProvider.of<AppCubit>(context);
    super.initState();
    _cubit.fetchListProcess();
    print('tree id ${widget.selectedTreeId ?? "null treeId"}');
    print('process id ${widget.selectedProcessId ?? "nullprocess"}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Chọn quy trình chăm sóc',
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(child: _buildListResult()),
          ],
        ),
      ),
    );
  }

  Widget _buildListResult() {
    return BlocBuilder<AppCubit, AppState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.getGardenStatus != current.getGardenStatus;
      },
      builder: (context, state) {
        if (state.getGardenStatus == LoadStatus.LOADING) {
          return Center(
            child: AppCircularProgressIndicator(),
          );
        } else {
          List<ProcessEntity> listProcess = state.processes!.where((element) {
            if (element.trees != null) {
              for (int i = 0; i < element.trees!.length; i++) {
                if (element.trees![i].tree_id == widget.selectedTreeId) {
                  return true;
                }
              }
              return false;
            } else {
              return false;
            }
          }).toList();
          for (dynamic e in listProcess) {
            print(e.process_id);
          }

          return ListView.separated(
            padding: EdgeInsets.only(top: 10),
            itemCount: listProcess.length,
            shrinkWrap: true,
            primary: false,
            separatorBuilder: (context, index) {
              return SizedBox(height: 10);
            },
            itemBuilder: (context, index) {
              final process = listProcess[index];
              String title = process.name!;
              bool isSelected = false;
              if (widget.selectedProcessId != null) if (process.process_id ==
                  widget.selectedProcessId) isSelected = true;
              return ItemWidget(
                  title: title,
                  isSelected: isSelected,
                  onTap: () {
                    Navigator.of(context).pop(process);
                  });
            },
          );
        }
      },
    );
  }
}
