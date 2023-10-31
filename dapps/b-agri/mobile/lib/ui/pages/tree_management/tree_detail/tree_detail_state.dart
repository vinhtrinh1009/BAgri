part of 'tree_detail_cubit.dart';

class TreeDetailState extends Equatable {
  LoadStatus? loadStatus;
  TreeEntity? treeData;

  TreeDetailState({
    this.loadStatus,
    this.treeData,
  });

  TreeDetailState copyWith({
    LoadStatus? loadStatus,
    TreeEntity? treeData,
  }) {
    return TreeDetailState(
      loadStatus: loadStatus ?? this.loadStatus,
      treeData: treeData ?? this.treeData,
    );
  }

  @override
  List<dynamic> get props => [
        loadStatus,
        treeData,
      ];
}
