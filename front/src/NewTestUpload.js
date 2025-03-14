import { useRef } from "react";
import { forwardRef } from "react";


const UploadProps = {
    onUpload: (data) => {},
    className: String,
    children: React.ReactNode,
    overlay: boolean,
    disabled: boolean,
  }
  
  export const UploadRef = {
    upload: () => {},
    abort: () => {}
  }
  
  export const Upload = forwardRef<UploadRef, UploadProps>(({ 
    onUpload,
    disabled,
    overlay = true,
    children,
    className
  }, ref) => {
    const [progress, setProgress] = useState(0);
    const [drop, setDrop] = useState(false);
    const [loading, setLoading] = useState(false);
  
    const abortUploading = useRef<() => void>();
    
    const abort = () => {
      abortUploading.current?.();
      reset();
    };
    
    const reset = () => {
      setLoading(false);
      setProgress(0);
    }
    
    const handleFile = (file) => {
      if (loading || !file) return;
    
      setLoading(true);
      const uploading = upload<T>(file, url, { onProgress: setProgress });
      abortUploading.current = uploading.abort;
      uploading
        .then(onUpload)
        .catch((e) => {})
        .finally(reset)
    };
  
    const onDragLeave = (e) => {
      if (disabled) return;
      e.preventDefault();
      setDrop(false);
    };
    
    const onDragOver = (e) => {
      if (disabled) return;
      e.preventDefault();
      setDrop(true);
    };
    
    const handleDrop = (e) => {
      if (disabled) return;
      e.preventDefault();
      const droppedFile = e.dataTransfer.files[0];
      setDrop(false);
    
      handleFile(droppedFile);
    };
  
    const handleFileChange = (event) => {
      handleFile(event.target.files[0]);
    };
  
    // Ссылка на инпут нужна для внешнего метода upload
    const input = useRef<HTMLInputElement>();
  
    useImperativeHandle(ref, () => ({
      // upload открывает документы для выбора файлов, другими словами
      // это то же самое что и нажатие на input
      upload: () => input.current?.click(),
      // функция abort уже готова, она сбрасывает отображение компонента
      abort,
    }));
  
    const id = useId()
    return (
      <div 
        className={cn(s.root, className)}
        onDrop={handleDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
      >
        {children}
        // добавили класс s.drop если drop
        <label htmlFor={id} className={cn(s.label, overlay && s.visible, drop && s.drop)}>
          <input
            ref={input}
            disabled={disabled}
            type="file"
            className={s.input}
            onChange={handleFileChange}
            id={id}
          />
          <UploadOutlined className={s.icon} />
        </label>
        {loading && (
          <div className={s.loading}>
            <LoadingOutlined className={s.icon} />
            <ProgressIndicator progress={progress} className={s.progress} theme="green" />
            <CloseCircleOutlined className={s.abort} onClick={abort} />
          </div>
        )}
      </div>
    );
  });
  
  Upload.displayName = "Upload";