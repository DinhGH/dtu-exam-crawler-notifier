import { useEffect, useState, useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../components/ui/Card";
import { toast } from "sonner";
import { subscriptionService } from "../../services/subscriptionService";
import { Modal } from "../../components/ui/Modal";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "../../components/ui/Table";

const subscriptionSchema = z.object({
  fullName: z.string().min(2, { message: "Họ tên phải có ít nhất 2 ký tự" }),
  email: z.string().email({ message: "Email không hợp lệ" }),
  subjectCode: z.string().optional(),
  subjectName: z.string().optional(),
});

const Register = () => {
  const form = useForm({
    resolver: zodResolver(subscriptionSchema),
    defaultValues: {
      fullName: "",
      email: "",
      subjectCode: "",
      subjectName: "",
    },
  });

  const [subscriptions, setSubscriptions] = useState([]);
  const [loadingList, setLoadingList] = useState(false);
  const [loadingAction, setLoadingAction] = useState(false);
  const [selected, setSelected] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [editData, setEditData] = useState({
    fullName: "",
    email: "",
    subjectCode: "",
    subjectName: "",
  });

  const hasLoaded = useRef(false);

  const fetchSubscriptions = async () => {
    try {
      setLoadingList(true);
      const data = await subscriptionService.getSubscriptions(0, 200);
      setSubscriptions(data || []);
    } catch (e) {
      console.error(e);
      toast.error("Không thể tải danh sách đăng ký");
    } finally {
      setLoadingList(false);
    }
  };

  useEffect(() => {
    if (hasLoaded.current) return;
    hasLoaded.current = true;

    const load = async () => {
      try {
        const data = await subscriptionService.getSubscriptions(0, 200);
        setSubscriptions(data || []);
      } catch (e) {
        console.error(e);
      }
    };

    load();
  }, []);

  const onSubmit = async (data) => {
    setLoadingAction(true);
    try {
      await subscriptionService.subscribe(data);
      toast.success("Đăng ký thành công!", {
        duration: 3000,
      });
      form.reset();
      // Chạy 1 lần duy nhất sau khi gửi
      await fetchSubscriptions();
    } catch {
      // toast is handled by apiClient
    } finally {
      setLoadingAction(false);
    }
  };

  const openViewModal = async (id) => {
    try {
      const sub = await subscriptionService.getSubscriptionById(id);
      setSelected(sub);
      setEditData({
        fullName: sub.full_name || sub.fullName || "",
        email: sub.email || "",
        subjectCode: sub.subject_code || "",
        subjectName: sub.subject_name || "",
      });
      setModalOpen(true);
    } catch (e) {
      console.error(e);
      toast.error("Không thể lấy thông tin đăng ký");
    }
  };

  const handleSave = async () => {
    if (!selected) return;
    setLoadingAction(true);
    try {
      await subscriptionService.updateSubscription(selected.id, {
        fullName: editData.fullName,
        email: editData.email,
        subjectCode: editData.subjectCode,
        subjectName: editData.subjectName,
      });
      toast.success("Cập nhật thành công");
      setModalOpen(false);
      fetchSubscriptions();
    } catch {
      // toast is handled by apiClient
    } finally {
      setLoadingAction(false);
    }
  };

  const handleDelete = async () => {
    if (!selected) return;
    setLoadingAction(true);
    try {
      await subscriptionService.deleteSubscription(selected.id);
      toast.success("Xóa thành công");
      setModalOpen(false);
      setDeleteModalOpen(false);
      fetchSubscriptions();
    } catch {
      // toast is handled by apiClient
    } finally {
      setLoadingAction(false);
    }
  };

  return (
    <div className="h-full w-full bg-white text-neutral-900 flex flex-col font-sans antialiased min-h-0">
      <main className="flex-1 p-4 min-h-0 bg-neutral-50/40">
        <div className="max-w-full mx-auto grid grid-cols-1 lg:grid-cols-12 gap-4 h-full items-stretch">
          <section className="lg:col-span-4 flex flex-col min-h-0">
            <Card className="border border-neutral-200 shadow-sm rounded-lg bg-white h-full flex flex-col overflow-hidden">
              <CardHeader className="space-y-1 border-b border-neutral-100 pb-4 pt-5 px-5 shrink-0">
                <CardTitle className="text-lg font-bold text-neutral-950 flex items-center gap-2">
                  <span className="w-1.5 h-5 bg-blue-600 rounded-md inline-block"></span>
                  Đăng ký nhận lịch thi
                </CardTitle>
              </CardHeader>

              <CardContent className="p-5">
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="space-y-4"
                >
                  <div className="space-y-1">
                    <label className="text-sm font-bold text-neutral-700 uppercase tracking-wider">
                      Họ và tên *
                    </label>
                    <Input
                      {...form.register("fullName")}
                      placeholder="Nguyễn Văn A"
                      className="border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 rounded-md text-sm placeholder-neutral-400 text-neutral-950 bg-white"
                      error={form.formState.errors?.fullName?.message}
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-sm font-bold text-neutral-700 uppercase tracking-wider">
                      Email nhận thông báo *
                    </label>
                    <Input
                      type="email"
                      {...form.register("email")}
                      placeholder="example@gmail.com"
                      className="border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 rounded-md text-sm placeholder-neutral-400 text-neutral-950 bg-white"
                      error={form.formState.errors?.email?.message}
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-sm font-bold text-neutral-700 uppercase tracking-wider">
                      Mã môn học (Tùy chọn)
                    </label>
                    <Input
                      {...form.register("subjectCode")}
                      placeholder="Ví dụ: CS 466 SA"
                      className="border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 rounded-md text-sm placeholder-neutral-400 text-neutral-950 bg-white"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-sm font-bold text-neutral-700 uppercase tracking-wider">
                      Tên môn học (Tùy chọn)
                    </label>
                    <Input
                      {...form.register("subjectName")}
                      placeholder="Ví dụ: Perl & Python"
                      className="border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 rounded-md text-sm placeholder-neutral-400 text-neutral-950 bg-white"
                    />
                  </div>

                  <Button
                    type="submit"
                    isLoading={loadingAction}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-md shadow-sm transition-colors duration-150 mt-2"
                  >
                    Kích hoạt giám sát
                  </Button>
                </form>
              </CardContent>
            </Card>
          </section>

          <section className="lg:col-span-8 flex flex-col min-h-0">
            <Card className="border border-neutral-200 shadow-sm rounded-lg bg-white h-full flex flex-col overflow-hidden">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 border-b border-neutral-100 py-4 px-5 shrink-0 bg-neutral-50/40">
                <div>
                  <CardTitle className="text-lg font-bold text-neutral-950">
                    Danh sách đang giám sát
                  </CardTitle>
                  <CardDescription className="text-neutral-500 text-xs mt-0.5">
                    Hiện có{" "}
                    <span className="font-bold text-neutral-950">
                      {subscriptions.length}
                    </span>{" "}
                    cấu hình theo dõi
                  </CardDescription>
                </div>
                <Button
                  onClick={fetchSubscriptions}
                  variant="outline"
                  size="sm"
                  className="border-neutral-300 text-neutral-700 hover:bg-neutral-100 rounded-md font-medium text-xs transition-colors"
                >
                  🔄 Làm mới
                </Button>
              </CardHeader>

              <CardContent className="p-0 flex-1 overflow-y-auto min-h-0 bg-white">
                {loadingList ? (
                  <div className="flex flex-col items-center justify-center h-full text-neutral-500 space-y-2">
                    <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                    <span className="text-xs font-medium">
                      Đang đồng bộ dữ liệu...
                    </span>
                  </div>
                ) : subscriptions.length === 0 ? (
                  <div className="flex items-center justify-center h-full text-neutral-400 text-xs italic">
                    Chưa có cấu hình theo dõi nào được kích hoạt.
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <Table className="w-full min-w-[600px]">
                      <TableHeader className="bg-neutral-50 sticky top-0 border-b border-neutral-200 z-10 shadow-sm">
                        <TableRow>
                          <TableHead className="font-bold text-neutral-900 text-sm uppercase tracking-wider">
                            Họ tên
                          </TableHead>
                          <TableHead className="font-bold text-neutral-900 text-sm uppercase tracking-wider">
                            Email
                          </TableHead>
                          <TableHead className="font-bold text-neutral-900 text-sm uppercase tracking-wider text-center">
                            Mã môn
                          </TableHead>
                          <TableHead className="font-bold text-neutral-900 text-sm uppercase tracking-wider text-center">
                            Tên môn
                          </TableHead>
                          <TableHead className="text-right font-bold text-neutral-900 text-sm uppercase tracking-wider pr-5">
                            Thao tác
                          </TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {subscriptions.map((s) => (
                          <TableRow
                            key={s.id}
                            className="hover:bg-neutral-50/60 border-b border-neutral-100 transition-colors"
                          >
                            <TableCell className="font-semibold text-neutral-950 text-sm">
                              {s.full_name}
                            </TableCell>
                            <TableCell className="text-neutral-600 font-mono text-sm">
                              {s.email}
                            </TableCell>
                            <TableCell className="text-center">
                              {s.subject_code ? (
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-sm font-semibold bg-neutral-100 text-neutral-800 border border-neutral-200">
                                  {s.subject_code}
                                </span>
                              ) : (
                                <span className="text-neutral-400 text-sm">
                                  -
                                </span>
                              )}
                            </TableCell>
                            <TableCell className="text-center text-sm text-neutral-600">
                              {s.subject_name || "-"}
                            </TableCell>
                            <TableCell className="text-right pr-5">
                              <div className="flex gap-1.5 justify-end">
                                <Button
                                  onClick={() => openViewModal(s.id)}
                                  size="sm"
                                  variant="outline"
                                  className="h-9 text-sm font-medium border-neutral-200 text-neutral-700 hover:bg-neutral-100 rounded"
                                >
                                  📝 Sửa
                                </Button>
                              </div>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>
          </section>
        </div>
      </main>

      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Cập Nhật Cấu Hình Đăng Ký"
      >
        {selected && (
          <div className="space-y-4 pt-1 text-gray-100">
            <div className="space-y-1">
              <label className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                Họ và tên sinh viên
              </label>
              <Input
                value={editData.fullName}
                className="rounded-md border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 text-neutral-950"
                onChange={(e) =>
                  setEditData((p) => ({ ...p, fullName: e.target.value }))
                }
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                Địa chỉ Email
              </label>
              <Input
                value={editData.email}
                className="rounded-md border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 text-neutral-950"
                onChange={(e) =>
                  setEditData((p) => ({ ...p, email: e.target.value }))
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                  Mã học phần
                </label>
                <Input
                  value={editData.subjectCode}
                  className="rounded-md border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 text-neutral-950"
                  onChange={(e) =>
                    setEditData((p) => ({ ...p, subjectCode: e.target.value }))
                  }
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                  Tên môn học
                </label>
                <Input
                  value={editData.subjectName}
                  className="rounded-md border-neutral-300 focus:border-blue-600 focus:ring-blue-600/10 text-neutral-950"
                  onChange={(e) =>
                    setEditData((p) => ({ ...p, subjectName: e.target.value }))
                  }
                />
              </div>
            </div>

            <div className="flex justify-end gap-2.5 border-t border-slate-800 pt-4 mt-6">
              <Button
                variant="ghost"
                onClick={() => setModalOpen(false)}
                className="rounded-md text-gray-900 hover:bg-white/5 text-xs font-medium"
              >
                Hủy bỏ
              </Button>
              <Button
                variant="destructive"
                onClick={() => setDeleteModalOpen(true)}
                className="bg-rose-500 hover:bg-rose-600 text-white rounded-md text-xs font-medium px-4"
              >
                Xóa đăng ký
              </Button>
              <Button
                onClick={handleSave}
                isLoading={loadingAction}
                className="bg-blue-600 hover:bg-blue-700 text-white rounded-md text-xs font-medium px-5 shadow-sm"
              >
                Lưu chỉnh sửa
              </Button>
            </div>
          </div>
        )}
      </Modal>

      <Modal
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        title="Xác nhận xóa"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Bạn có chắc chắn muốn xóa đăng ký này?
          </p>
          <div className="flex justify-end space-x-3">
            <Button variant="ghost" onClick={() => setDeleteModalOpen(false)}>
              Hủy
            </Button>
            <Button
              className="bg-red-600 hover:bg-red-700 text-white"
              onClick={handleDelete}
              isLoading={loadingAction}
            >
              Xác nhận xóa
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Register;
