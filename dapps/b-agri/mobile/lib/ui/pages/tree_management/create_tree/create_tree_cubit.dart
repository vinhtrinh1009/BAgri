import 'package:bloc/bloc.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/process/create_process_params.dart';
import 'package:flutter_base/models/params/trees/create_tree_params.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/repositories/tree_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:equatable/equatable.dart';
import 'package:rxdart/rxdart.dart';
part 'create_tree_state.dart';

class CreateTreeCubit extends Cubit<CreateTreeState> {
  TreeRepository? treeRepository;

  CreateTreeCubit({
    this.treeRepository,
  }) : super(CreateTreeState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void changeName(String name) {
    emit(state.copyWith(name: name));
  }

  void changeDescription(String description) {
    emit(state.copyWith(description: description));
  }

  void createTree() async {
    emit(state.copyWith(createTreeStatus: LoadStatus.LOADING));
    try {
      final param =
          CreateTreeParam(name: state.name, description: state.description);
      final response = await treeRepository!.createTree(param: param);

      if (response != null) {
        emit(state.copyWith(createTreeStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(createTreeStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      emit(state.copyWith(createTreeStatus: LoadStatus.FAILURE));
      return;
    }
  }
}
