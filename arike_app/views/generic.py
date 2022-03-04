from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView

from arike_app.views.mixins import ModelTabViewMixin


class GenericModelListView(ModelTabViewMixin, FilterView):
    view_type = "list"

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def has_permission(self) -> bool:
        return super().has_permission() and self.model.has_read_permission(self.request)


class GenericModelDetailView(ModelTabViewMixin, DetailView):
    view_type = "details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_update_perm"] = self.get_object().has_object_update_permission(self.request)
        return context

    def has_permission(self) -> bool:
        return super().has_permission() and self.get_object().has_object_read_permission(self.request)


class GenericModelUpdateView(ModelTabViewMixin, UpdateView):
    view_type = "edit"
    success_url = "../"

    def has_permission(self) -> bool:
        return super().has_permission() and self.get_object().has_object_update_permission(self.request)


class GenericModelDeleteView(ModelTabViewMixin, DeleteView):
    view_type = "delete"
    success_url = "../../"

    def has_permission(self) -> bool:
        return super().has_permission() and self.model.has_delete_permission(self.request)


class GenericModelCreateView(ModelTabViewMixin, CreateView):
    view_type = "create"
    success_url = "../"

    def has_permission(self) -> bool:
        return super().has_permission() and self.model.has_create_permission(self.request)
