#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStandardItemModel>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onPdfClicked();
    void onCsvClicked();
    void onDestClicked();
    void onGenerateClicked();
    void checkGenerateEnabled();

private:
    QString scriptPath() const;

private:
    Ui::MainWindow *ui;
    QStandardItemModel m_model;
    QString m_lastPath;
};
#endif // MAINWINDOW_H
