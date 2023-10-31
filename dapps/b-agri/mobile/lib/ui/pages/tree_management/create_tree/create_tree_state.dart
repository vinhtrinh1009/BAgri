part of 'create_tree_cubit.dart';

class CreateTreeState extends Equatable {
  final String? name;
  final String? description;
  final LoadStatus? createTreeStatus;

  const CreateTreeState({
    this.name,
    this.description,
    this.createTreeStatus,
  });

  CreateTreeState copyWith({
    String? name,
    final String? description,
    LoadStatus? createTreeStatus,
  }) {
    return CreateTreeState(
      name: name ?? this.name,
      description: description ?? this.description,
      createTreeStatus: createTreeStatus ?? this.createTreeStatus,
    );
  }

  @override
  List<Object?> get props => [
        this.name,
        this.description,
        this.createTreeStatus,
      ];
}
